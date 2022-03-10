import requests
import traceback
import os
import os.path
import datetime
import ssl
import certifi
import os
import shutil
import hashlib
import re

from sqlalchemy.orm import Session
from urllib import request
from bs4 import BeautifulSoup

from .get_or_create import get_or_create
from ...database import models


class Downloader:

    def __init__(self, db: Session, path_to_error_log='errors/downloadErrorLog.csv', base_file_dir='xls/'):
        self.url = 'https://www.mirea.ru/schedule/'
        self.path_to_error_log = path_to_error_log
        self.base_file_dir = base_file_dir
        self.file_type = ['xls', 'xlsx']
        self.db = db

    def get_period(self, file_name: str):
        file_name = file_name.upper()
        if "ЗАЧ" in file_name and not 'ЭКЗ' in file_name:
            return "credits"
        if 'ЭКЗ' in file_name or 'СЕСС' in file_name:
            return "exams"
        if 'ЗИМА' in file_name and not 'ИТХТ' in file_name:
            return "exams"
        else:
            return "semester"

    def get_period_id(self, file_name: str):
        file_name = file_name.upper()
        if "ЗАЧ" in file_name and not 'ЭКЗ' in file_name:
            return 2
        if 'ЭКЗ' in file_name or 'СЕСС' in file_name:
            return 3
        if 'ЗИМА' in file_name and not 'ИТХТ' in file_name:
            return 3
        else:
            return 1

    def get_inst(self, file_name: str):
        file_name = file_name.upper()
        if "ИПТИП" in file_name:
            return 1
        if "ИТУ" in file_name:
            return 2
        if "ИИТ" in file_name:
            return 3
        if "ИИИ" in file_name:
            return 4
        if "ИКБ" in file_name:
            return 5
        if "ИРЭИ" in file_name:
            return 6
        return 7

    def get_year(self, file_name: str):
        file_name = file_name.upper()
        return int(re.search(r'\d(?= *К)', file_name)[0])

    def is_mag(self, file_name: str):
        file_name = file_name.upper()
        return "МАГ" in file_name

    def get_place(self, file_name: str):
        temp_file_name = file_name.lower()
        if "стром" in temp_file_name or "кбисп" in temp_file_name or "икб" in temp_file_name or ("иту" in temp_file_name and "сем" in temp_file_name):
            return 3
        elif "итхт" in temp_file_name:
            return 2
        else:
            return 1

    def download(self):
        #urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
        response = request.urlopen(self.url, context=ssl.create_default_context(
            cafile=certifi.where()))  # Запрос страницы
        site = str(response.read().decode())  # Чтение страницы в переменную
        response.close()

        # Объект BS с параметром парсера
        parse = BeautifulSoup(site, "html.parser")
        # xls_list = parse.findAll('a', {"class": "xls"})  # поиск в HTML Всех классов с разметой Html
        # поиск в HTML Всех классов с разметой Html
        xls_list = parse.findAll('a', {"class": "uk-link-toggle"})

        # Списки адресов на файлы
        # Сохранение списка адресов сайтов
        url_files = [x['href'].replace('https', 'http') for x in xls_list]

        # Сохранение файлов
        # print(self.base_file_dir)
        if not os.path.exists(self.base_file_dir):
            os.makedirs(self.base_file_dir)
        else:
            shutil.rmtree(self.base_file_dir)
            os.makedirs(self.base_file_dir)
        hashes = self.db.query(models.FileHash).all()
        hashes = [h.name for h in hashes]

        for url_file in url_files:  # цикл по списку
            divided_path = os.path.split(url_file)
            # subdir = os.path.split(divided_path[0])[1]
            subdir = ''
            file_name = subdir + divided_path[1]
            if "КОЛЛЕ" in file_name.upper() or "УЗ" in file_name.upper():
                continue

            try:
                if os.path.splitext(file_name)[1].replace('.', '') in self.file_type and "заоч" not in os.path.splitext(file_name)[0].replace('.', ''):
                    subdir = self.get_period(file_name.upper())
                    # print(subdir)

                    # print(path_to_file)

                    if not os.path.isdir(os.path.join(self.base_file_dir, subdir)):
                        os.makedirs(os.path.join(
                            self.base_file_dir, subdir), exist_ok=False)
                    
                    h = hashlib.sha1()

                    with requests.get(url_file, stream=True) as r:
                        r.raise_for_status()
                        # loop till the end of the file
                        chunk = 0
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                h.update(chunk)

                    hash = get_or_create(session=self.db, model=models.FileHash,
                                        name=file_name)
                    if hash.hash == h.hexdigest():
                        print("skip", file_name)

                    else:
                        print(hash.hash, "!=", h.hexdigest())
                        hash.hash = h.hexdigest()
                        self.db.commit()
                    # return the hex representation of digest
                    
                    # with open(download_path, 'wb') as f:
                    #     for chunk in r.iter_content(chunk_size=8192):
                    #         if chunk:
                    #             f.write(chunk)
                        with requests.get(url_file, stream=True) as r:
                            subdir = self.get_period(file_name.upper())
                            path_to_file = os.path.join(
                                self.base_file_dir, subdir, file_name)
                            r.raise_for_status()
                            if os.path.isfile(path_to_file):
                                os.remove(path_to_file)
                            with open(path_to_file, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:
                                        f.write(chunk)
                        print("download", file_name)

            except Exception as err:
                traceback.print_exc()
                with open(self.path_to_error_log, 'a+') as file:

                    file.write(
                        str(datetime.datetime.now()) + ': ' + url_file + ' message:' + str(err) + '\n', )
                pass


if __name__ == "__main__":
    Downloader = Downloader(
        path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/', except_types=[])
    Downloader.download()
