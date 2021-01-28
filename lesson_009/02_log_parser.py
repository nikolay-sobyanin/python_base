# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

from abc import ABC, abstractmethod
from collections import defaultdict


class LogParser(ABC):

    def __init__(self, file_name_in=None, file_name_out=None):
        self.file_name_in = file_name_in
        self.file_name_out = file_name_out
        self.list_log = []
        self.list_result = defaultdict(int)

    def parser(self):
        self.read_file()
        self.group_events()
        self.write_result_file()

    def read_file(self):
        with open(file=self.file_name_in, mode='r', encoding='utf8') as file:
            for line in file:
                self.list_log.append(self.parser_line(line=line))

    @abstractmethod
    def parser_line(self, line):
        pass

    def group_events(self):
        for log in self.list_log:
            if log['status'] == 'NOK':
                self.list_result[log['time']] += 1

    def write_result_file(self):
        with open(file=self.file_name_out, mode='w', encoding='utf8') as file:
            for time, res in self.list_result.items():
                line = f'{time} {res}\n'
                file.write(line)
        print(f'Файл результатов {self.file_name_out} создан.')


class ParserMinute(LogParser):
    def __str__(self):
        return 'отказов в минуту'

    def parser_line(self, line):
        date = line[1:11]
        time = line[12:17]
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        hour = time[0:2]
        minute = time[3:5]
        status = line[29:-1]
        return {
            'time': f'{year}-{month}-{day} {hour}:{minute}',
            'status': status
        }


class ParserHour(LogParser):
    def __str__(self):
        return 'отказов в час'

    def parser_line(self, line):
        date = line[1:11]
        time = line[12:17]
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        hour = time[0:2]
        status = line[29:-1]
        return {
            'time': f'{year}-{month}-{day} {hour}:00',
            'status': status
        }


class ParserDay(LogParser):
    def __str__(self):
        return 'отказов в день'

    def parser_line(self, line):
        date = line[1:11]
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        status = line[29:-1]
        return {
            'time': f'{year}-{month}-{day}',
            'status': status
        }


class ParserMonth(LogParser):
    def __str__(self):
        return 'отказов в месяц'

    def parser_line(self, line):
        date = line[1:11]
        year = date[0:4]
        month = date[5:7]
        status = line[29:-1]
        return {
            'time': f'{year}-{month}',
            'status': status
        }


file_name_in = 'events.txt'
file_name_out = 'out.txt'

list_parser = [ParserMinute, ParserHour, ParserDay, ParserMonth]

while True:
    for i, elm in enumerate(list_parser, 1):
        print(f'{i} - {elm().__str__()}')

    enter_sort = input('Как групировать: ')
    if not enter_sort.isdigit():
        print('Используйте только цифры!')
        continue
    if not 1 <= int(enter_sort) <= len(list_parser):
        print('Неверно введено значение!')
        continue

    list_parser[int(enter_sort) - 1](file_name_in, file_name_out).parser()
    break


# После зачета первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
