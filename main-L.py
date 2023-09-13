from PIL import Image
from pathlib import Path
from datetime import *
from time import sleep
import telebot
from Logger import *



rootdir = r'D:\data\decoded'
logs_dir = r'C:\Users\lorett\Documents\telegram-archive-of-satellite-images\logs'

TOKEN = '5094120884:AAHZKdwfNtH5FVD9EdoIOgVhMIsqngfM4y4'
chat = "@L_ArchiveFAST"

send_chat_2 = False
chat_2 = '@PlanumMobileArchiveFAST'

name_station = 'PlanumYerevan'



compression_ratio = 4

dawn = time(6, 0, 0, 0) # рассвет
sunset = time(15, 0, 0, 0) # закат

dict_path = {}

Image.MAX_IMAGE_PIXELS = None


def rmtree(f: Path):
    if f.is_file():
        f.unlink()
    else:
        for child in f.iterdir():
            rmtree(child)
        f.rmdir()


def dirSize(root: Path):
    return sum(f.stat().st_size for f in root.glob('**/*') if f.is_file())


def resized_image(image_in: Path, image_out: Path, compression_ratio: int):
    image = Image.open(str(image_in))
    resized_image = image.resize((image.size[0]//compression_ratio, image.size[1]//compression_ratio))
    resized_image.save(image_out, optimize=True)


logs = Logger('L_bot_fast', logs_dir, loggingLevels['debug'])

bot = telebot.TeleBot(TOKEN)
logs.info('start telegram client')

while True:
    for path in sorted(Path(rootdir).iterdir()):
        if dirSize(path) > 0 and path.is_dir():
            if path not in dict_path.keys():
                dict_path[path] = [dirSize(path), 0, False]
                logs.info(f'new file - {str(path)}')

            elif path in dict_path.keys() and dict_path[path][0] == dirSize(path):
                dict_path[path][1] += 1

            elif path in dict_path.keys() and dict_path[path][0] != dirSize(path):
                dict_path[path][0] = dirSize(path)
            #     dict_path[path][2] = False

            if dict_path[path][1] >= 40 and not dict_path[path][2]:
                try:
                    hour_record = int(str(path)[str(path).index('_') + 1: str(path).index('_') + 3])
                    minute_record = int(str(path)[str(path).index('_') + 3: str(path).index('_') + 5])
                    time_record = time(hour_record, minute_record, 0, 0)
                        
                    if ('NOAA' in str(path) or 'METOP' in str(path)) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + r'\AVHRR\avhrr_3_rgb_221_corrected.png')
                        name_out = Path(str(path) + r'\AVHRR\avhrr_3_rgb_221_corrected_compress.png')                    
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        if send_chat_2:
                            bot.send_photo(chat_id=chat_2, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(20)

                    elif 'NOAA' in str(path) or 'METOP' in str(path):
                        name_in = Path(str(path) + r'\AVHRR\avhrr_3_rgb_3b45_corrected.png')
                        name_out = Path(str(path) + r'\AVHRR\avhrr_3_rgb_3b45_corrected_compress.png')                    
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        if send_chat_2:
                            bot.send_photo(chat_id=chat_2, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        logs.info(f'send file - {str(name_out)}') 
                        dict_path[path][2] = True
                        sleep(20)

                    elif ('METEOR' in str(path)) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + r'\MSU-MR\msu_mr_rgb_221_corrected.png')
                        name_out = Path(str(path) + r'\MSU-MR\msu_mr_rgb_221_corrected_compress.png')                    
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        if send_chat_2:
                            bot.send_photo(chat_id=chat_2, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                           
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(20)

                    elif 'METEOR' in str(path):
                        name_in = Path(str(path) + r'\MSU-MR\msu_mr_rgb_456_corrected.png')
                        name_out = Path(str(path) + r'\MSU-MR\msu_mr_rgb_456_corrected_compress.png')                    
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        
                        if send_chat_2:
                            bot.send_photo(chat_id=chat_2, photo=open(str(name_out), 'rb'),  caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')

                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(20)
                        
                except:
                    logs.error(f'error send image {str(path)}') 
                    # dict_path[path][2] = True
                    
    sleep(2)
    # logs.info(f'{str(dict_path)}') 