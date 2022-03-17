from .orm_reader import Reader
from .downloader import Downloader
from .predefined import create_predefined


def parse_schedule(db, test_mode=False):
    try:
        create_predefined(db=db)

        if test_mode:
            downloader = Downloader(db=db, path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='tests/files/')
        else:
           downloader = Downloader(db=db, path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/')

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

    except FileNotFoundError as err:
        print("Ошибка! Не найдены файлы исходного расписания")

    except Exception as err:
        print("Ошибка открытия файла!\n")
        print(err)
