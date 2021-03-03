# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
import math
import os
from operator import itemgetter
from multiprocessing import Process, Queue
from queue import Empty
from library.utils import time_track


class SecidParcer(Process):

    def __init__(self, file_paths, holder,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_paths = file_paths
        self.holder = holder

    def parse_line(self, line):
        line = line.rstrip()
        secid, tradetime, full_price, quantity = line.split(',')
        price = float(full_price) / int(quantity)
        return secid, price

    def run(self):
        for file_path in self.file_paths:
            with open(file_path, 'r', encoding='utf8') as file:
                file.readline()
                name_secid, price = self.parse_line(file.readline())
                max_price = min_price = price
                for line in file:
                    _, price = self.parse_line(line)
                    if price > max_price:
                        max_price = price
                    elif price < min_price:
                        min_price = price
            half_sum = (max_price + min_price) / 2
            volatility = ((max_price - min_price) / half_sum) * 100
            self.holder.put((name_secid, volatility))


class SecidManager:
    def __init__(self, dir_path, quantity_performer):
        self.dir_path = dir_path
        self.quantity_performer = quantity_performer
        self.holder = Queue(maxsize=self.quantity_performer * 4)
        self.list_file_paths = []
        self.dict_volatility = {}
        self.zero_volatility = []

    def start_manager(self):
        self.get_file_paths()
        self.run_performers(quantity_performer=self.quantity_performer)
        self.output_result()

    def get_file_paths(self):
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                self.list_file_paths.append(os.path.join(dirpath, file))

    def run_performers(self, quantity_performer):
        size_part = math.ceil(len(self.list_file_paths) / quantity_performer)
        parts = [self.list_file_paths[size_part * i:size_part * (i + 1)] for i in range(quantity_performer)]

        performers = [SecidParcer(file_paths=part, holder=self.holder) for part in parts]
        for performer in performers:
            performer.start()

        while True:

            # Изначально делал вот так. Почему это не сработало я понял так.
            # В самом конце почему то процесс последний выдавал что он еще "живой".
            # И получалось так, что он делал еще одну итерацию цикла и блокировался на функции get,
            # которая бесконечно ожидает элемента из очереди, которого там уже не будет.

            # Вопрос.
            # Почему не сработало в конце условие: not any(performer.is_alive() for performer in performers)?

            #  зависало?
            #  Скорее всего срабатывал такой сценарий: Исполнители все что могли отдали, и завершают, или хотя бы
            #  один из них (процесс не завершают за 1 нс, уходит некоторое время, пока он может быть жив). За это время
            #  Менеджер взял из очереди последний элемент, проверил, что есть живой и начал ждать следующий элемент,
            #  который никогда не придет, т.к. Исполнители вот-вот "умрут".
            #  .
            #  get`у нужно добавить таймаут.

            # secid = self.holder.get()
            # print(secid)
            # if secid[1] == 0:
            #     self.zero_volatility.append(secid[0])
            # else:
            #     self.dict_volatility[secid[0]] = secid[1]
            # if not any(performer.is_alive() for performer in performers):
            #     break

            try:
                secid, volatility = self.holder.get(timeout=0.05)
                if volatility == 0:
                    self.zero_volatility.append(secid)
                else:
                    self.dict_volatility[secid] = volatility
            except Empty:
                if not any(performer.is_alive() for performer in performers):
                    break

        for performer in performers:
            performer.join()

    def output_result(self):
        sort_dict = [i for i in sorted(self.dict_volatility.items(), key=itemgetter(1), reverse=True)]
        max_volatility = sort_dict[:3]
        min_volatility = sort_dict[-3:]
        print(len(self.dict_volatility) + len(self.zero_volatility), len(self.list_file_paths))
        print(f'{"Результат":*^30}')
        print('Максимальная волатильность:')
        for secid, volatility in max_volatility:
            print(f'{secid} - {round(volatility, 2):^5} %')
        print()
        print('Минимальная волатильность:')
        for secid, volatility in min_volatility:
            print(f'{secid} - {round(volatility, 2):^5} %')
        print()
        print('Нулевая волатильность:')
        self.zero_volatility.sort()
        print(', '.join(self.zero_volatility))


dir_path = 'trades'
dir_path = os.path.normpath(dir_path)


@time_track
def main():
    SecidManager(dir_path=dir_path, quantity_performer=4).start_manager()


if __name__ == '__main__':
    main()

# зачет!