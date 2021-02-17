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


class LogParser(ABC):

    def __init__(self, file_name_in):
        self.file_name_in = file_name_in

    def __iter__(self):
        self.file = open(file=self.file_name_in, mode='r', encoding='utf8')
        self.count = 0
        self.basic_time = None
        self.current_line = None
        return self

    def __next__(self):
        while True:
            if self.current_line is None:
                self.current_line = self.file.readline()
            self.basic_time, basic_status = self.parser_line(line=self.current_line)
            if basic_status == 'NOK':
                self.count = 1
            else:
                self.count = 0
            for line in self.file:
                time, status = self.parser_line(line=line)
                if time == self.basic_time:
                    if status == 'NOK':
                        self.count += 1
                    continue
                self.current_line = line
                if self.count == 0:  # Не генерируем значения с 0.
                    break
                return self.basic_time, self.count
            else:
                break  # Достигли конца файла выходим из цикла while.
        self.file.close()
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
