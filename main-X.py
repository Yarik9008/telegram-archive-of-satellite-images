from PIL import Image
from pathlib import Path
from pprint import pprint
from datetime import *
from time import sleep
import telebot
from telebot import types
from Logger import *



rootdir = r'C:\Users\Yarik\YandexDisk\lorett\dataX'
logs_dir = r'C:\Users\Yarik\Documents\telegram-archive-of-satellite-images\logs'

TOKEN = '5094120884:AAHZKdwfNtH5FVD9EdoIOgVhMIsqngfM4y4'
chat = "@X_ArchiveFAST"

name_station = 'R3-test'

compression_ratio = 7

dawn = time(6, 0, 0, 0) # рассвет
sunset = time(17, 0, 0, 0) # закат

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
    resized_image = image.resize(
        (image.size[0]//compression_ratio, image.size[1]//compression_ratio))
    resized_image.save(image_out, optimize=True)


logs = Logger('X_bot_fast', logs_dir, loggingLevels['debug'])

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

            # elif path in dict_path.keys() and dict_path[path][0] != dirSize(path):
            #     dict_path[path][0] = dirSize(path)
            #     dict_path[path][2] = False

            if dict_path[path][1] >= 10 and not dict_path[path][2]:
                # try:
                    hour_record = int(str(path)[str(path).index('_') + 1: str(path).index('_') + 3])
                    minute_record = int(str(path)[str(path).index('_') + 3: str(path).index('_') + 5])
                    second_record = int(str(path)[str(path).index('_') + 3: str(path).index('_') + 5])
                    time_record = time(hour_record, minute_record, 0, 0)

                    if 'FENGYUN 3D' in str(path) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + '\MERSI-2\mersi2_rgb_321_corrected.png')
                        name_out = Path(str(path) + '\MERSI-2\mersi2_rgb_321_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'FENGYUN 3D' in str(path):
                        name_in = Path(str(path) + '\MERSI-2\mersi2_5_Equalized_corrected.png')
                        name_out = Path(str(path) + '\MERSI-2\mersi2_5_Equalized_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)

                    if 'FENGYUN 3F' in str(path) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + '\MERSI-3\mersi3_rgb_321_corrected.png')
                        name_out = Path(str(path) + '\MERSI-3\mersi3_rgb_321_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'FENGYUN 3F' in str(path):
                        name_in = Path(str(path) + '\MERSI-3\mersi3_5_Equalized_corrected.png')
                        name_out = Path(str(path) + '\MERSI-3\mersi3_5_Equalized_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'FENGYUN 3E' in str(path) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + '\MERSI-LL\mersill_rgb_338_corrected.png')
                        name_out = Path(str(path) + '\MERSI-LL\mersill_rgb_338_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'FENGYUN 3E' in str(path):
                        name_in = Path(str(path) + '\MERSI-LL\mersill_IR_DNB_Mix_corrected.png')
                        name_out = Path(str(path) + '\MERSI-LL\mersill_IR_DNB_Mix_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    # elif 'FENGYUN 3G' in str(path) and time_record >= dawn and time_record <= sunset:
                    #     name_in = Path(str(path) + '\MERSI-RM\mersill_rgb_338_corrected.png')
                    #     name_out = Path(str(path) + '\MERSI-RM\mersill_rgb_338_corrected_compress.png')
                    #     resized_image(name_in, name_out, 7)
                    #     bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                    #     logs.info(f'send file - {str(path)}')
                        
                    # elif 'FENGYUN 3G' in str(path) and time_record < dawn and time_record > sunset:
                    #     name_in = Path(str(path) + '\MERSI-RM\mersill_IR_DNB_Mix_corrected.png')
                    #     name_out = Path(str(path) + '\MERSI-RM\mersill_IR_DNB_Mix_corrected_compress.png')
                    #     resized_image(name_in, name_out, 7)
                    #     bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                    #     logs.info(f'send file - {str(path)}')
                                            
                    elif 'TERRA' in str(path) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + '\MODIS\modis_rgb_143_corrected.png')
                        name_out = Path(str(path) + '\MODIS\modis_rgb_143_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)

                        
                    elif 'TERRA' in str(path):
                        name_in = Path(str(path) + '\MODIS\modis_rgb_Day_Microphysics_corrected.png')
                        name_out = Path(str(path) + '\MODIS\modis_rgb_Day_Microphysics_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)

                    elif 'AQUA' in str(path) and time_record >= dawn and time_record <= sunset:
                        name_in = Path(str(path) + '\MODIS\modis_rgb_143_corrected.png')
                        name_out = Path(str(path) + '\MODIS\modis_rgb_143_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'AQUA' in str(path):
                        name_in = Path(str(path) + '\MODIS\modis_rgb_Day_Microphysics_corrected.png')
                        name_out = Path(str(path) + '\MODIS\modis_rgb_Day_Microphysics_corrected_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                    elif 'NOAA 20' in str(path) and time_record >= dawn and time_record <= sunset:
                        pass
                        # name_in = Path(str(path) + '\MODIS\modis_rgb_143_corrected.png')
                        # name_out = Path(str(path) + '\MODIS\modis_rgb_143_corrected_compress.png')
                        # resized_image(name_in, name_out, 7)
                        # bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        # logs.info(f'send file - {str(name_out)}')
                        
                    elif 'NOAA 20' in str(path):
                        name_in = Path(str(path) + r'\VIIRS\viirs_Thermal_Channel.png')
                        name_out = Path(str(path) + r'\VIIRS\viirs_Thermal_Channel_compress.png')
                        resized_image(name_in, name_out, compression_ratio)
                        bot.send_photo(chat_id=chat, photo=open(str(name_out), 'rb'), caption = f'Name station: {name_station}\nName pass: {str(path)[len(rootdir) + 1:]}')
                        logs.info(f'send file - {str(name_out)}')
                        dict_path[path][2] = True
                        sleep(2)
                        
                # except:
                #     logs.error(f'error send image {str(path)}') 
                             
    sleep(1)
    logs.info(f'{str(dict_path)}') 



