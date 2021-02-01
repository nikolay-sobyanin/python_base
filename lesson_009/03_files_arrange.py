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
from abc import abstractmethod, ABC


class SortFiles(ABC):
    def __init__(self, dir_from, dir_to):
        # TODO: почему строку ниже можно заменить и все работает?
        #  Докопайтесь почему.
        #self.dir_from = os.path.normpath(os.path.join(os.path.dirname(__file__), dir_from))    # было
        self.dir_from = os.path.normpath(dir_from)                                              # стало

        self.dir_to = os.path.normpath(os.path.join(os.path.dirname(__file__), dir_to))



    def sort_files(self):
        for dirpath, dirnames, filenames in os.walk(self.dir_from): # TODO: в архиве os.walk работать не будет
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                self.copy_file(file_path=file_path)

    @abstractmethod
    def copy_file(self, file_path):
        pass


class SortFilesByTime(SortFiles):
    def copy_file(self, file_path):
        # TODO: используйте распаковку для file_time.
        file_time = time.gmtime(os.path.getmtime(file_path))
        # TODO: чтобы тут подставить переменную с понятным именем вместо "file_time[0]"
        path_copy_file = os.path.join(self.dir_to, str(file_time[0]), str(file_time[1]))
        if not os.path.isdir(path_copy_file):
            os.makedirs(path_copy_file)
        shutil.copy2(src=file_path, dst=path_copy_file)


dir_from = 'icons'
dir_to = 'icons_by_year'

SortFilesByTime(dir_from=dir_from, dir_to=dir_to).sort_files()
print(f'Скрипт сработал. Файлы записаны в дерикторию "{dir_to}"')



# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html

# TODO: если есть запал - можно начинать) скучно не будет точно (как по мне, 9.3 - одна из самых сложных задач за весь
#  курс).
