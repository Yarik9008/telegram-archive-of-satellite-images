from PIL import Image
from pathlib import Path
from datetime import *
from time import sleep
import telebot
from Logger import *
from pathlib import Path
from pprint import pprint
import shutil
from telethon import TelegramClient, sync
import requests


# rootdir = r'C:/Users/Yarik/YandexDisk/лоретт/ДАННЫЕ/PlanumMobile/'
# logs_dir = r'C:\Users\Yarik\Documents\telegram-archive-of-satellite-images\logs'


# def upload_portal(path_file:str):
#     with open(path_file, 'rb') as f:
#         files = {
#             'file': f
#             }
#         form = {
#             'station':'planumMobileGood',
#             'ftype':'generic',
#         }

#         res = requests.post('http://proc.lorett.org/file_post', files=files, data=form)
#         print(res.text)
          

# dict_path = {}

# def rmtree(f: Path):
#     if f.is_file():
#         f.unlink()
#     else:
#         for child in f.iterdir():
#             rmtree(child)
#         f.rmdir()

# def dirSize(root: Path):
#     return sum(f.stat().st_size for f in root.glob('**/*') if f.is_file())

# logs = Logger('Upload_dat', logs_dir, loggingLevels['debug'])

# # for zipPath in sorted(list(map(lambda a: str(a), Path(rootdir).glob('*.zip')))):
# #     try:
# #         print(zipPath)
# #         shutil.unpack_archive(filename=zipPath, extract_dir=zipPath[:-4], format="zip")
# #     except:
# #         pass

# for path in sorted(Path(rootdir).iterdir()):
#     if 'NOAA' in (str(path)) and '.' not in (str(path)):
#         name_raw = str(path) + '/noaa_hrpt.raw16'
#         name_dat = str(path) + '/' + str(path)[52 : 90] + '.raw16'
#         shutil.copyfile(name_raw, name_dat)
#         print(name_dat)
#         # upload_portal(name_dat)
        
            