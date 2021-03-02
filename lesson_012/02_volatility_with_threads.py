# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
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


import os
from operator import itemgetter
from threading import Thread
from queue import Queue
from library.utils import time_track


class SecidParcer(Thread):

    def __init__(self, file_paths, holder_dict, holder_list,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_paths = file_paths
        self.dict_volatility = {}
        self.zero_volatility = []
        self.holder_dict = holder_dict
        self.holder_list = holder_list

    def parser_line(self, line):
        line = line.rstrip()
        secid, tradetime, full_price, quantity = line.split(',')
        price = float(full_price) / int(quantity)
        return secid, price

    def run(self):
        for file_path in self.file_paths:
            with open(file_path, 'r', encoding='utf8') as file:
                file.readline()
                name_secid, price = self.parser_line(file.readline())
                max_price, min_price = price, price
                for line in file:
                    price = self.parser_line(line)[1]
                    if price > max_price:
                        max_price = price
                    elif price < min_price:
                        min_price = price
            half_sum = (max_price + min_price) / 2
            volatility = ((max_price - min_price) / half_sum) * 100

            if volatility == 0:
                self.zero_volatility.append(name_secid)
                continue
            self.dict_volatility[name_secid] = volatility

        self.holder_dict.put(self.dict_volatility)
        self.holder_list.put(self.zero_volatility)


class SecidManager:
    def __init__(self, dir_path, quantity_performer):
        self.dir_path = dir_path
        self.quantity_performer = quantity_performer
        self.list_file_paths = []
        self.dict_volatility = {}
        self.zero_volatility = []
        # TODO: создавать очереди для поток не обязательно. Все создаваемые потоки находятся в одном процессе,
        #  т.к. в одном контексте. Это значит, что можно буквально запросить любое поле у Исполнителя и он его выдаст.
        #  Добавление очереди не принесыт выгоды, а только замедлит работу.
        self.holder_dict = Queue(maxsize=self.quantity_performer)
        self.holder_list = Queue(maxsize=self.quantity_performer)

    def start_manager(self):
        self.get_file_paths()
        self.run_performers(quantity_performer=self.quantity_performer)
        self.output_result()

    def get_file_paths(self):
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                self.list_file_paths.append(os.path.join(dirpath, file))

    def run_performers(self, quantity_performer):
        size_part = len(self.list_file_paths) // quantity_performer
        parts = [self.list_file_paths[size_part * i:size_part * (i + 1)] for i in range(quantity_performer - 1)]
        parts.append(self.list_file_paths[(quantity_performer - 1) * size_part:])

        performers = [SecidParcer(part, self.holder_dict, self.holder_list) for part in parts]
        for performer in performers:
            performer.start()

        while any(performer.is_alive() for performer in performers):
            holder_dict = self.holder_dict.get()
            holder_list = self.holder_list.get()
            self.dict_volatility.update(holder_dict)
            self.zero_volatility.extend(holder_list)

        for performer in performers:
            performer.join()

    def output_result(self):
        sort_keys = [i[0] for i in sorted(self.dict_volatility.items(), key=itemgetter(1), reverse=True)]
        max_volatility_keys = sort_keys[:3]
        min_volatility_keys = sort_keys[-3:]
        print(len(self.dict_volatility) + len(self.zero_volatility), len(self.list_file_paths))
        print(f'{"Результат":*^30}')
        print('Максимальная волатильность:')
        for key in max_volatility_keys:
            print(f'{key} - {round(self.dict_volatility[key], 2):^5} %')
        print()
        print('Минимальная волатильность:')
        for key in min_volatility_keys:
            print(f'{key} - {round(self.dict_volatility[key], 2):^5} %')
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
