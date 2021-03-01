# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
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
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>
import os
from operator import itemgetter
from library.utils import time_track


class SecidParcer:

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.dict_volatility = {}
        self.zero_volatility = []

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


class SecidManager:
    def __init__(self, dir_path, quantity_performer):
        self.dir_path = dir_path
        self.quantity_performer = quantity_performer
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
        size_part = len(self.list_file_paths) // quantity_performer
        parts = [self.list_file_paths[size_part * i:size_part * (i + 1)] for i in range(quantity_performer - 1)]
        parts.append(self.list_file_paths[(quantity_performer - 1) * size_part:])
        count_files = sum(map(lambda x: len(x), parts))
        print(f'Всего файлов проверено: {count_files}. А должно быть проверено: {len(self.list_file_paths)}')
        for i, part in enumerate(parts, 1):
            print(f'Размер части №{i} - {len(part)}')
            parser_files = SecidParcer(file_paths=part)
            parser_files.run()
            self.dict_volatility.update(parser_files.dict_volatility)
            self.zero_volatility.extend(parser_files.zero_volatility)

    def output_result(self):
        sort_keys = [i[0] for i in sorted(self.dict_volatility.items(), key=itemgetter(1), reverse=True)]
        max_volatility_keys = sort_keys[:3]
        min_volatility_keys = sort_keys[-3:]
        print()
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


