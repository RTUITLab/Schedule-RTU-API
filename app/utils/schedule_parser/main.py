from sqlalchemy import MetaData
from sqlalchemy import create_engine

from .orm_reader import Reader
from .downloader import Downloader
from .predefined import create_predefined

from ...dependencies import get_settings


def parse_schedule(db):
    try:
        engine = create_engine(get_settings().database_url,
                            encoding='utf-8', echo=True)
        
        meta = MetaData()

        connection = engine.connect()
        connection.execute( '''TRUNCATE TABLE specific_week CASCADE''' )
        connection.execute( '''TRUNCATE TABLE lesson CASCADE''' )
        connection.execute( '''TRUNCATE TABLE discipline CASCADE''' )
        connection.execute( '''TRUNCATE TABLE "group" CASCADE''' )
        connection.execute( '''TRUNCATE TABLE room CASCADE''' )
        connection.execute( '''TRUNCATE TABLE teacher CASCADE''' )

        connection.close()
    
        print("truncate")
        
        create_predefined(db=db)

        Download = Downloader(db=db, path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/')
        # Download.download()

        print("downloaded")
        try:
            reader = Reader(db)
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
