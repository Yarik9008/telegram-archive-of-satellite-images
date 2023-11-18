from PIL import Image
from pathlib import Path
from datetime import *
from time import sleep
import telebot
import json
from Logger import *
from requests import get, post
from pprint import pprint 
import os


def rmtree(f: Path):
    if f.is_file():
        f.unlink()
    else:
        for child in f.iterdir():
            rmtree(child)
        f.rmdir()


def dirSize(root: Path):
    return int(sum(f.stat().st_size for f in root.glob('**/*') if f.is_file())) // ( 1024 * 1024)


def flip_imege(image_in: Path, image_out: Path, flip_angle: int) -> None:
    image = Image.open(str(image_in))
    flipped_image = image.rotate(angle=flip_angle)
    flipped_image.save(image_out, optimize=True)


def resized_image(image_in: Path, image_out: Path, compression_ratio: int):
    image = Image.open(str(image_in))
    resized_image = image.reduce(compression_ratio)
    resized_image.save(image_out)


def main():
    while True:
        
        passPath = sorted(Path(config['data_directory']).iterdir())
        
        passList = open("C:/Lorett_lband/telegram-archive-of-satellite-images/pass_list.txt", 'r').readlines()
        
        checkNew = False
        
        newPath = []
        
        for i in passPath:
            if str(i) + '\n' not in passList and i.is_dir():
                checkNew = True
                newPath.append(i)
                logs.info(f"new pass: {str(i)}")
                
        
        if checkNew:
        
            for path in newPath:
                
                passList = open("C:/Lorett_lband/telegram-archive-of-satellite-images/pass_list.txt", 'r').readlines()

                if str(path) + '\n' not in passList:
                    
                    logs.info(f"pass not in file: {str(path)}")
                
                    timeMoment = datetime.strptime(str(path)[len(config['data_directory']) + 1 : len(config['data_directory']) + 16], '%Y%m%d_%H%M%S')
                    difference = int((datetime.now() - timeMoment).total_seconds())
                    timeDay = time(hour=timeMoment.hour, minute=timeMoment.minute, second=timeMoment.second)
                    
                    if difference >= config['difference']:
                        
                        logs.info(f"difference correct: {str(path)}")
                        
                        name_image_in = Path(str(path)+ config['satList'][str(path.name).rsplit("_")[2]]['day_product'])
                        
                        checkIm = False 
                        
                        if os.path.exists(str(name_image_in)) and os.path.getsize(str(name_image_in)) / ( 1024 * 1024) >= 1.5 and difference >= 3600:
                            checkIm = True
                            logs.info('checkIm = True')
                            
                        elif difference >= 3600:
                            
                            with open("C:/Lorett_lband/telegram-archive-of-satellite-images/pass_list.txt", 'a+') as file_pass:
                                file_pass.write(str(path) + '\n')
                                logs.info(f'no correct')
                                
                            continue
                        
                        else:
                                                            
                            for i in range(120):
                                if os.path.exists(str(name_image_in)) and os.path.getsize(str(name_image_in)) / ( 1024 * 1024) >= 1.5:
                                    print(os.path.getsize(str(name_image_in)) / ( 1024 * 1024))
                                    checkIm = True
                                    logs.info('checkIm = True')
                                    sleep(5)
                                    break
                                else:
                                    logs.info('sleep 1')
                                    sleep(5)
                        
                        if checkIm:

                            if timeDay >= dawn and timeDay <= sunset:
                                
                                name_image_in = Path(str(path)+ config['satList'][str(path.name).rsplit("_")[2]]['day_product'])
                                name_image_out = Path(str(path) + config['satList'][str(path.name).rsplit("_")[2]]['day_product'][:-4] + '_compress.png')
                                product = config['satList'][str(path.name).rsplit("_")[2]]['day_product']
                                    
                            else:
                                
                                name_image_in = Path(str(path) + config['satList'][str(path.name).rsplit("_")[2]]['night_product'])
                                name_image_out = Path(str(path) + config['satList'][str(path.name).rsplit("_")[2]]['night_product'][:-4] + '_compress.png')              
                                product = str(config['satList'][str(path.name).rsplit("_")[2]]['day_product']).rsplit("/")[2]
                                
                            resized_image(name_image_in, name_image_out, config['compression_ratio'])
                            
                            sleep(config['delay'])
                                
                            try:
                                difference = int((datetime.now() - timeMoment).total_seconds())
                                
                                bot.send_photo(chat_id=config['chat_fast'], photo=open(str(name_image_out), 'rb'),
                                        caption=f'Location: {config["location"]}\nStation: {config["name_station"]}\nPass: {path.name}\nProduct: {product}\nDifference: {str(timedelta(seconds=difference))}')
                                    
                                logs.info(f'send product: {str(name_image_out)}')

                            except:
                                logs.error(f'error send product: {str(name_image_out)}')

                        else:
                            logs.info(f'low size pass: {str(path)}')
                            
                        
                        with open("C:/Lorett_lband/telegram-archive-of-satellite-images/pass_list.txt", 'a+') as file_pass:
                                file_pass.write(str(path) + '\n')
                                logs.info(f'pass append to file')
                                                
                    else:
                        logs.info(f"less difference: {str(path)}")
                        
                else:
                    logs.info(f"pass in file: {str(path)}")
        else:
            logs.debug(f'no new pass')
            
        sleep(10)
        # logs.debug(f'active: {str(datetime.now())}')
                    
                    
                    
if __name__ == "__main__":
    
    with open("C:/Lorett_lband/telegram-archive-of-satellite-images/config_arch_bot.json", 'r') as file_config:
        config = json.load(file_config)
       
    dawn = time(hour=config['dawn_utc']['hour'], minute=config['dawn_utc']['minute'], second=config['dawn_utc']['second'])  # рассвет
    sunset = time(hour=config['sunset_utc']['hour'], minute=config['sunset_utc']['minute'], second=config['sunset_utc']['second'])  # закат

    Image.MAX_IMAGE_PIXELS = None

    logs = Logger('fast bot', str(os.path.dirname(os.path.abspath(__file__))) + '/.logs', loggingLevels['debug'])

    bot = telebot.TeleBot(config['TOKEN'])
    bot.remove_webhook()
    
    logs.info('Start telegram bot')
            
    main()