# -*- coding: utf-8 -*-

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# (время создания файла берется по разному в разых ОС - см https://clck.ru/PBCAX - поэтому берем время модификации).
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит, см .gitignore в папке ДЗ)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4


import os
import time
import shutil
import zipfile
from abc import abstractmethod, ABC


class SortFiles(ABC):
    def __init__(self, dir_from, dir_to):
        self.dir_from = os.path.normpath(dir_from)
        self.dir_to = os.path.normpath(dir_to)

    def sort_files(self):
        for file in self.get_files():
            self.copy_file(file=file)

    @abstractmethod
    def get_files(self):
        pass

    @abstractmethod
    def copy_file(self, file):
        pass


class SortFolderByTime(SortFiles):
    def get_files(self):
        list_path_files = []
        for dirpath, dirnames, filenames in os.walk(self.dir_from):
            for file in filenames:
                list_path_files.append(os.path.join(dirpath, file))
        return list_path_files

    def copy_file(self, file):
        file_time = time.gmtime(os.path.getmtime(file))
        path_copy_file = os.path.join(self.dir_to, str(file_time.tm_year), str(file_time.tm_mon))
        if not os.path.isdir(path_copy_file):
            os.makedirs(path_copy_file)
        shutil.copy2(src=file, dst=path_copy_file)


class SortZipByTime(SortFiles):
    def get_files(self):
        with zipfile.ZipFile(self.dir_from, 'r') as zip_file:
            return zip_file.infolist()

    def copy_file(self, file):
        with zipfile.ZipFile(self.dir_from, 'r') as zip_file:
            path = zipfile.Path(zip_file.filename, file.filename)
            if path.is_file():
                path_unpacking_file = os.path.join(self.dir_to, str(file.date_time[0]), str(file.date_time[1]))
                if not os.path.isdir(path_unpacking_file):
                    os.makedirs(path_unpacking_file)
                file.filename = path.name
                zip_file.extract(file, path_unpacking_file)


dir_from = 'icons'
dir_to = 'icons_by_year'

if os.path.isdir(dir_from):
    SortFolderByTime(dir_from, dir_to).sort_files()
    print(f'Скрипт сработал. Файлы записаны в дерикторию "{dir_to}"')
elif zipfile.is_zipfile(dir_from):
    dir_to += '_zip'
    SortZipByTime(dir_from, dir_to).sort_files()
    print(f'Скрипт сработал. Файлы записаны в дерикторию "{dir_to}"')
else:
    print('Error')

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
