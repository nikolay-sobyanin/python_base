# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>  # Итератор или генератор? выбирайте что вам более понятно
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234

from abc import ABC, abstractmethod
from collections import defaultdict


class LogParser(ABC):

    def __init__(self, file_name_in):
        self.file_name_in = file_name_in

    def __iter__(self):
        self.list_time_group = []
        self.file = open(file=self.file_name_in, mode='r', encoding='utf8')
        self.count = 0
        self.basic_time = None
        return self

    def __del__(self):
        self.file.close()

    def __next__(self):
        self.file.seek(0)
        for line in self.file:
            time, status = self.parser_line(line=line)
            if status != 'NOK':
                continue
            if time in self.list_time_group:
                continue
            self.basic_time = time
            self.count = 1
            for line in self.file:
                time, status = self.parser_line(line=line)
                if status != 'NOK':
                    continue
                if time == self.basic_time:
                    self.count += 1
            self.list_time_group.append(self.basic_time)
            return self.basic_time, self.count
        raise StopIteration

    @abstractmethod
    def parser_line(self, line):
        pass


class ParserMinute(LogParser):
    def parser_line(self, line):
        return '[' + line[1:17] + ']', line[29:-1]


grouped_events = ParserMinute('events.txt')
for time, count in grouped_events:
    print(time, count)
print('Закончил работу')
