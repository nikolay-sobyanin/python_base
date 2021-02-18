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

            # TODO: тут можно немного упростить.
            #  int(True) == 1
            #  int(False) == 0
            #  .
            #  Мы можем избавиться от условия.
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

        # TODO: не факт, что итератор дойдет до конца. Нужно найти место, где закрывать файл, если он был открыт.
        #  ВНИМАНИЕ: проблема в том, что файл может быть открыт 100500 раз, а закроется не каждый раз.
        #  Подсказка: прежде чем "переоткрыть", стоит ...
        self.file.close()
        raise StopIteration

        # TODO: вообще стоит оговориться:
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