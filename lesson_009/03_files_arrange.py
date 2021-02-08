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
        for file_path in self.get_files():
            if self.is_dir(file_path):
                continue
            destination_dir = self.create_dir(file_path)
            self.copy_file(file_path, destination_dir)

    @abstractmethod
    def get_files(self):
        pass

    @abstractmethod
    def is_dir(self, file_path):
        pass

    @abstractmethod
    def create_dir(self, file_path):
        pass

    @abstractmethod
    def copy_file(self, file_path, destination_dir):
        pass


class SortFolderByTime(SortFiles):

    def get_files(self):
        list_path_files = []
        for dirpath, dirnames, filenames in os.walk(self.dir_from):
            for file in filenames:
                list_path_files.append(os.path.join(dirpath, file))
        return list_path_files

    def is_dir(self, file_path):
        return os.path.isdir(file_path)

    def create_dir(self, file_path):
        file_time = time.gmtime(os.path.getmtime(file_path))
        path_copy_file = os.path.join(self.dir_to, str(file_time.tm_year), str(file_time.tm_mon))
        if not os.path.isdir(path_copy_file):
            os.makedirs(path_copy_file)
        return path_copy_file

    def copy_file(self, file_path, destination_dir):
        shutil.copy2(src=file_path, dst=destination_dir)


class SortZipByTime(SortFiles):
    def __init__(self, dir_from, dir_to):
        super().__init__(dir_from, dir_to)
        self.zip_file = zipfile.ZipFile(self.dir_from)

    def __del__(self):
        self.zip_file.close()

    def get_files(self):
        return self.zip_file.namelist()

    def is_dir(self, file_path):
        return self.zip_file.getinfo(file_path).is_dir()

    def create_dir(self, file_path):
        info_file = self.zip_file.getinfo(file_path)
        path_unpacking_file = os.path.join(self.dir_to, str(info_file.date_time[0]), str(info_file.date_time[1]))
        if not os.path.isdir(path_unpacking_file):
            os.makedirs(path_unpacking_file)
        return path_unpacking_file

    def copy_file(self, file_path, destination_dir):
        with self.zip_file.open(file_path) as file_from:
            with open(os.path.join(destination_dir, os.path.basename(file_path)), 'wb') as file_to:
                shutil.copyfileobj(file_from, file_to)


dir_from = 'icons.zip'
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

#  Открытие файлов через with.
#     Можно вкладывать друг в друга:
#           with open(...) as f_1:
#               with open(...) as f_2:
#                   line_file_1 = f_1.readline()
#                   line_file_2 = f_2.readline()
#     .
#     А можно использовать следующий синтаксис:
#           with open("1.txt") as f1, open("2.txt") as f2:
#               line_file_1 = f_1.readline()
#               line_file_2 = f_2.readline()
#     .
#     Если вложенности кода небольшая - первый вариант лучше. Если большая - только второй.

# зачет!