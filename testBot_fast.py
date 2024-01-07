from pathlib import Path
from requests import get, post
from PIL import Image
from time import sleep
from datetime import *
from Logger import *
import json
import os
import telebot
import asyncio
from re import fullmatch
from pprint import pprint
from telebot.types import InputMediaPhoto
from pyppeteer import launch


# какой-то костыль чтобы сжимать фотки 
Image.MAX_IMAGE_PIXELS = None

class FastBot:
    # инициализация 
    def __init__(self) -> None:
        # инициализация логера 
        self.logs = Logger('arch_bot_fast', "/home/lorett/telegram-archive-of-satellite-images/.logs", loggingLevels['debug'])

        # подтягивание конфига 
        with open("/home/lorett/telegram-archive-of-satellite-images/config_bot.json", 'r') as file_config:
            self.config = json.load(file_config)
            self.logs.info(self.config)
            # рассвет
            self.dawn = time(hour=self.config['dawn_utc']['hour'], minute=self.config['dawn_utc']
                        ['minute'], second=self.config['dawn_utc']['second'])  
            # закат
            self.sunset = time(hour=self.config['sunset_utc']['hour'], minute=self.config['sunset_utc']
                        ['minute'], second=self.config['sunset_utc']['second'])
            # токен телеграмм бота 
            token = self.config['TOKEN']
            # чат для отправки снимков
            self.chat = self.config['chat_fast']
            # директория где ожидаются снимки 
            self.data_directory = self.config['data_directory']
            # список проверенных диреторий 
            self.old_directories = []
            # коэф сжатия 
            self.compression = self.config['compression']
            # список спутников для которых есть конфиг 
            self.sat_list = []
            for i in self.config['sat_list_x'].keys():
                self.sat_list.append(i)
            # конфиг для спутников 
            self.sat_config = self.config['sat_list_x']
            # минимальная задержка 
            self.difference = int(self.config['difference'])
            # минимальный размер папки с файлами 
            self.min_size = int(self.config['min_size'])
            # задержка между инерациями цикла 
            self.delay = int(self.config['delay'])
            
        # инициализация бота
        self.bot = telebot.TeleBot(token)
        self.logs.info('start telegram bot')
        
        
        
    # рекурсивное удаление директории и всего её содержимого (работает)
    def rmtree(self, data_path: Path):
        if data_path.is_file():     
            data_path.unlink()
            
        else:
            for child in data_path.iterdir():
                self.rmtree(child)
            data_path.rmdir()
            
        self.logs.info(f'delite: {str(data_path)}')
        
    # измерение размера файла или директории, выводит в МБ
    def dir_size(self, data_path: Path):
        return int(sum(f.stat().st_size for f in data_path.glob('**/*') if f.is_file())) // (1024 * 1024)
    
    # переворот изображения если это необходимо 
    def image_orientation_normalization(self, image_path: Path):
        pass
    
    # сжатие изображения (не проверено)
    def image_compression(self, image_path: Path):
        self.logs.info(f'image compression in: {str(image_path)}')
        image = Image.open(str(image_path))
        resized_image = image.reduce(self.compression)
        image_out = str(image_path)[:-4] + '_compress.png'
        resized_image.save(image_out)
        self.logs.info(f'image compression out: {image_out}')
        
        return Path(image_out)
    
    # вычисление времени с начала пролета до текущего момента по имени
    def calculate_delay(self, data_path):
        timeMoment = datetime.strptime(str(data_path)[len(str(self.data_directory)) + 1: len(str(self.data_directory)) + 16], '%Y%m%d_%H%M%S')
        return int((datetime.utcnow() - timeMoment).total_seconds())
    
    # проверка директории на наличие новых вложенных директорий (проверенно)
    def checking_new_data(self):
        new_data = []
        
        old_directories = self.read_pass_list()
        
        for i in sorted(Path(self.data_directory).iterdir()):
            if i not in old_directories:
                new_data.append(i)
                self.logs.info(f'new directory: {str(i)}')
                
        return new_data
    
    # добавление в pass list
    def append_pass_list(self, data_path: Path):
        with open(str(os.path.dirname(os.path.abspath(__file__))) + "/pass_list_fast.txt", 'a+') as file_pass:
            file_pass.write(str(data_path) + '\n')
            self.logs.info(f'append to pass list: {str(data_path)}')
    
    # чтение pass list 
    def read_pass_list(self):
        return [Path(i[:-1]) for i in open(str(os.path.dirname(os.path.abspath(__file__))) + "/pass_list_fast.txt", 'r').readlines()]
    
    def get_log_image(self, data_path: Path):
    
        name = str(data_path).split('/')[-1].replace(' ', '_')
        
        async def main():
            browser = await launch(options={'args': ['--no-sandbox']})
            page = await browser.newPage()
            await page.goto(f'http://eus.lorett.org/eus/log_view/RastoropshaLite0__{name}_rec.log')
            await page.setViewport(viewport={'width': 620, 'height': 680})
            sleep(0.5)
            await page.screenshot({'path': f'{str(os.path.dirname(os.path.abspath(__file__)))}/log_image/{name}.png'})
            await browser.close()

        asyncio.get_event_loop().run_until_complete(main())
        
        return Path(f'{str(os.path.dirname(os.path.abspath(__file__)))}/log_image/{name}.png')

    # публикация в канал 
    def send(self, data_path: Path):
        # парсинг имени папки 
        datetimeMoment = datetime.strptime(str(data_path)[len(self.data_directory) + 1: len(self.data_directory) + 16], '%Y%m%d_%H%M%S')
        timeMoment = time(hour=datetimeMoment.hour, minute=datetimeMoment.minute, second=datetimeMoment.second)
        sat_name = str(data_path).split('_')[-1]
        
        if timeMoment >= self.dawn and timeMoment <= self.sunset:
            image_name = Path(str(data_path) + self.sat_config[sat_name]['day_product'])
        else:
            image_name = Path(str(data_path) + self.sat_config[sat_name]['night_product'])
            
        if not os.path.isfile(image_name):
            self.logs.error(f'no file: {str(image_name)}')
            self.append_pass_list(data_path)
            return 
        
        product = str(image_name).split('/')[-1]
        pass_sat = str(data_path).split('/')[-1]
        
        try: 
            self.bot.send_media_group(chat_id=self.chat, 
                                    media=[
                                        InputMediaPhoto(open(str(self.image_compression(image_name)), 'rb'), 
                                            caption = f'Location: {self.config["location"]}\nStation: {self.config["name_station"]}\nSatellite: {sat_name}\nPass: {pass_sat}\nProduct: {product}\nDifference: {timedelta(seconds=self.calculate_delay(data_path))}'),
                                        InputMediaPhoto(open(str(self.get_log_image(data_path)), 'rb'))
                                    ])
        
            self.logs.info(f'send image: {str(data_path)}')
            
        except:   
            self.logs.error('send error')
        
        self.append_pass_list(data_path)
              
    # основной цикл программмы 
    def main(self):
        while True:
            # проверяем на новые папки в отслежуемой дирректории 
            new_data = self.checking_new_data()
            
            pass_list = self.read_pass_list()
            
            # обрабатываем все новые папки 
            for directory in new_data:
                
                self.logs.info(f'directory: {str(directory)}')
                
                # проверка на наличие в pass list (исключение повторной отправки)
                if directory in pass_list:
                    continue
                
                # проверка на корректность имени 
                if (fullmatch('\d{8}_\d{6}', str(directory)[len(str(self.data_directory)) + 1 : len(str(self.data_directory)) + 16]) == None):
                    self.logs.error(f'no correct name directory: {str(directory)}')
                    self.append_pass_list(str(directory))
                    continue
                
                # проверка наличие конфига для спутника 
                if str(directory).split('_')[-1] not in self.sat_list:
                    self.logs.error(f'no config sat: {str(directory)}')
                    self.append_pass_list(str(directory))
                    continue
                
                # ожидаем до минимальной задержки 
                while self.calculate_delay(directory) < self.difference:
                    self.logs.debug('no minimum delay, sleep 5s')
                    sleep(5)
        
                # проверка на минимальный размер 
                if self.dir_size(directory) < self.min_size:
                    # удаляем и скипаем 
                    self.rmtree(directory)
                    continue
                
                # отправка после прохождения всех проверок
                self.send(directory)
                
                # задержка между отправками сообщений 
                sleep(5)
                
            self.logs.debug(f'sleep {self.delay}s')
            sleep(self.delay)
            
            
if __name__ == "__main__":
    bot = FastBot()
    bot.main()

