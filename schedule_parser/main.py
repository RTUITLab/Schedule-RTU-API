from .postgres_reader import Reader
from .downloader import Downloader
import sys
import os.path
import json


def parse_schedule():
    global Downloader
    try:
        # Download = Downloader(path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/')
        # Download.download()

        print("downloaded")
        try:
            reader = Reader()
        except:
            print("Reader error")
        print("start reading")
        reader.run('xls')
        print("\nКонвертация успешно выполнена!\n\n")

    except FileNotFoundError as err:
        print("Ошибка! Не найден файл шаблона 'template.xlsx' или файлы исходного расписания")

    except Exception as err:
        print("Ошибка открытия файла!\n")
        print(err.args)
