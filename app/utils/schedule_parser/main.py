import os
import shutil

from .orm_reader import Reader
from .downloader import Downloader
from .predefined import create_predefined
# from sqlalchemy import MetaData
# from sqlalchemy import create_engine
# from ...dependencies import get_settings


def parse_schedule(db, test_mode=False):
    try:
        # engine = create_engine(get_settings().database_url,
        #                     encoding='utf-8', echo=True)

        # meta = MetaData()

        # connection = engine.connect()
        # connection.execute( '''TRUNCATE TABLE specific_week CASCADE''' )
        # connection.execute( '''TRUNCATE TABLE lesson CASCADE''' )
        # connection.execute( '''TRUNCATE TABLE discipline CASCADE''' )
        # connection.execute( '''TRUNCATE TABLE "group" CASCADE''' )
        # connection.execute( '''TRUNCATE TABLE room CASCADE''' )
        # connection.execute( '''TRUNCATE TABLE teacher CASCADE''' )

        # connection.close()

        create_predefined(db=db)
        if test_mode:
            base_file_dir = 'tests/files/'
            print("test_mode")
        else:
            print("not test_mode")
            base_file_dir = 'xls/'

        downloader = Downloader(
            db=db, path_to_error_log='logs/downloadErrorLog.csv', base_file_dir=base_file_dir)
        downloader.download()

        print("downloaded")
        try:
            reader = Reader(db)
        except Exception as err:
            print("Reader error -> ", err)
        print("start reading")
        if test_mode:
            reader.run('tests/xls')
        else:
            reader.run('xls')
        print("\nКонвертация успешно выполнена!\n\n")
        try:
            if os.path.exists(base_file_dir):
                shutil.rmtree(base_file_dir)
        except Exception as e:
            print("Ошибка при очистке файлов", e)

    except FileNotFoundError as err:
        print("Ошибка! Не найдены файлы исходного расписания")

    except Exception as err:
        print("Ошибка открытия файла!\n")
        print(err)
