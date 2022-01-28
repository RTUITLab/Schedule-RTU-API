import contextlib
import sys
import os.path
import json

from .orm_reader import Reader
from .downloader import Downloader
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from os import environ 


def parse_schedule(without_weeks=True):
    global Downloader
    try:
        engine = create_engine(environ.get('CONNECTION_STRING'),
                            encoding='utf-8', echo=True)
        
        meta = MetaData()

        connection = engine.connect()
        connection.execute( '''TRUNCATE TABLE lesson_on_week CASCADE''' )
        connection.execute( '''TRUNCATE TABLE lesson CASCADE''' )
        connection.execute( '''TRUNCATE TABLE discipline CASCADE''' )
        connection.execute( '''TRUNCATE TABLE "group" CASCADE''' )
        connection.execute( '''TRUNCATE TABLE room CASCADE''' )
        connection.execute( '''TRUNCATE TABLE place CASCADE''' )
        connection.execute( '''TRUNCATE TABLE lesson_type CASCADE''' )
        connection.execute( '''TRUNCATE TABLE teacher CASCADE''' )
        connection.execute( '''TRUNCATE TABLE call CASCADE''' )
        connection.execute( '''TRUNCATE TABLE period CASCADE''' )
        connection.close()
    
        print("truncate")
        Download = Downloader(path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/')
        # Download.download()

        print("downloaded")
        try:
            reader = Reader()
        except Exception as err:
            print("Reader error -> ", err)
        print("start reading")
        reader.run('xls')
        print("\nКонвертация успешно выполнена!\n\n")

    except FileNotFoundError as err:
        print("Ошибка! Не найдены файлы исходного расписания")

    except Exception as err:
        print("Ошибка открытия файла!\n")
        print(err)
