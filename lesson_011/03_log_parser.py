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
        self.file = open(file=self.file_name_in, mode='r', encoding='utf8')

    # Добавил, что бы смоделировать ситуацию открытия файла.
    def read_two_line(self):
        print(self.file.readline(), end='')
        print(self.file.readline(), end='')
        # self.file.close()

    def __del__(self):
        self.file.close()

    def __iter__(self):
        print(f'Файл закрыт: {self.file.closed}.')
        if not self.file.closed:
            print('Закрыли файл.')
            self.file.close()
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
            self.count = int(basic_status == 'NOK')
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
                self.file.close()
                break  # Достигли конца файла выходим из цикла while.
        print(f'Файл закрыт: {self.file.closed}.')
        raise StopIteration

    @abstractmethod
    def parser_line(self, line):
        pass


class ParserMinute(LogParser):
    def parser_line(self, line):
        return '[' + line[1:17] + ']', line[29:-1]


grouped_events = ParserMinute('events.txt')
grouped_events.read_two_line()
for time, count in grouped_events:
    print(time, count)
print('Закончил работу')


# вообще стоит оговориться:
#  Мы с вами работаем в интерпретаторе CPython. Т.е. ядро написано на Си. Для этой версии файл закрывается
#  сам, если его забыли закрыть, а программа завершилась.
#  .
#  Но помимо CPython есть ядро на Java, Jython и на С# - IronPython.
#  Язык везде, в каждом интепретаторе будет python, но ядро написано будет на разных языках, и в отличии
#  от CPython, остальные версии не закрывают файлы за собой. Поэтому документация настоятельно рекомендует
#  контролировать закрытие файлов. Особенно это критично, если открывается куча файлов, в 12ом модуле нас
#  это ждет. Для текущей задачи, может я и излишне требователен, но раз документация требует - надо делать,
#  иначе на собесе любую аргументацию разобьют словами "документация рекомендует закрывать файл" или
#  "значит ваш код стабильно будет работать только под CPython?". Поэтому лучше не создавать бреши в своей
#  "броне надежности".
#  .
#  в конце файла прямая наводка, свертись, когда придумаете как закрыть файл.

# не читать если еще не сделали закрытие файла!
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .
# прежде чем открыть файл, можно проверить "а не открыт ли он уже" и закрыть если это так.
# .
# .
# .
# .
# .
# .
# .
# .
# .
# .