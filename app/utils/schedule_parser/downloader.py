from urllib import request
import requests
import traceback
import os
import os.path
import datetime
from bs4 import BeautifulSoup
import ssl
import certifi

import shutil



class Downloader:

    def __init__(self, path_to_error_log='errors/downloadErrorLog.csv', base_file_dir='xls/'):
        self.url = 'https://www.mirea.ru/schedule/'
        self.path_to_error_log = path_to_error_log
        self.base_file_dir = base_file_dir
        self.file_type = ['xls', 'xlsx']

    def get_dir(self, file_name):
        if "ЗАЧ" in file_name and not 'ЭКЗ' in file_name:
            return "credits"
        if 'ЭКЗ' in file_name or 'СЕСС' in file_name:
            return "exams"
        if 'ЗИМА' in file_name and not 'ИТХТ' in file_name: 
            return "exams"
        else:
            return "semester"

    
    def save_file(self, url, path):
        def download(download_url, download_path):
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                if os.path.isfile(download_path):
                    os.remove(download_path)
                with open(download_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        try:
            download(url, path)
            return "download"
        except:
            return "skip"

    def download(self):
        #urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
        response = request.urlopen(self.url, context=ssl.create_default_context(cafile=certifi.where()))  # Запрос страницы
        site = str(response.read().decode())  # Чтение страницы в переменную
        response.close()

        parse = BeautifulSoup(site, "html.parser")  # Объект BS с параметром парсера
        # xls_list = parse.findAll('a', {"class": "xls"})  # поиск в HTML Всех классов с разметой Html
        xls_list = parse.findAll('a', {"class": "uk-link-toggle"})  # поиск в HTML Всех классов с разметой Html
        
        # Списки адресов на файлы
        url_files = [x['href'].replace('https', 'http') for x in xls_list]  # Сохранение списка адресов сайтов
        progress_all = len(url_files)

        count_file = 0
        # Сохранение файлов
        print(self.base_file_dir)
        if not os.path.exists(self.base_file_dir):
            os.makedirs(self.base_file_dir)
        else:
            shutil.rmtree(self.base_file_dir)
            os.makedirs(self.base_file_dir)

        for url_file in url_files:  # цикл по списку
            divided_path = os.path.split(url_file)
            # subdir = os.path.split(divided_path[0])[1]
            subdir = ''
            file_name = subdir + divided_path[1]
            if "КОЛЛЕ" in file_name.upper() or "УЗ" in file_name.upper():
                continue
            
            try:
                if os.path.splitext(file_name)[1].replace('.', '') in self.file_type and "заоч" not in os.path.splitext(file_name)[0].replace('.', ''):
                    subdir = self.get_dir(file_name.upper())
                    print(subdir)
                    path_to_file = os.path.join(self.base_file_dir, subdir, file_name)
                    print(path_to_file)

                    if not os.path.isdir(os.path.join(self.base_file_dir, subdir)):
                        os.makedirs(os.path.join(self.base_file_dir, subdir), exist_ok=False)
                    result = self.save_file(url_file, path_to_file)
                    count_file += 1  # Счетчик для отображения скаченных файлов в %

                    print('{} : {} -- {}'.format(result, path_to_file, count_file / progress_all * 100))

                else:
                    count_file += 1  # Счетчик для отображения скаченных файлов в %

            except Exception as err:
                traceback.print_exc()
                with open(self.path_to_error_log, 'a+') as file:
                    file.write(
                        str(datetime.datetime.now()) + ': ' + url_file + ' message:' + str(err) + '\n', )
                pass


if __name__ == "__main__":
    Downloader = Downloader(path_to_error_log='logs/downloadErrorLog.csv', base_file_dir='xls/', except_types=[])
    Downloader.download()
