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


class SecidVolatility:

    # TODO: пусть принимает список файлов. Идея в том, чтобы можно было разделить 100500 файлов на 4 кучки и запустить
    #  4 исполнителя. В однопоточной версии это бессмысленно, но пригодится в 02 и 03 задачах.
    def __init__(self, file_path):
        self.file_path = file_path
        self.name_secid = None
        self.volatility = None

    def parser_line(self, line):
        line = line.rstrip()
        secid, tradetime, full_price, quantity = line.split(',')    # TODO: распаковка всегда дает доп.очки.
        price = float(full_price) / int(quantity)                   #  те, кто пишет не на питоне, а пришел в питон
        return secid, price                                         #  ею не пользуются.

    def run(self):
        with open(self.file_path, 'r', encoding='utf8') as file:
            file.readline()

            # TODO: Отгадайте с одной попытки какое поле можно заменить локальной переменной?
            self.name_secid, price = self.parser_line(file.readline())
            max_price, min_price = price, price
            for line in file:
                price = self.parser_line(line)[1]
                if price > max_price:
                    max_price = price
                elif price < min_price:
                    min_price = price
        half_sum = (max_price + min_price) / 2
        self.volatility = ((max_price - min_price) / half_sum) * 100


def file_paths(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            yield os.path.join(dirpath, file)


dict_volatility = {}
zero_volatility = []

dir_path = 'trades'
dir_path = os.path.normpath(dir_path)


# TODO: упаковать в класс Менеджер. Пусть этот класс создает Исполнителей (SecidVolatility). (см ниже)
@time_track
def main():
    secides = [SecidVolatility(file_path=file_path) for file_path in file_paths(dir_path=dir_path)]

    for secid in secides:
        secid.run()
        if secid.volatility == 0:
            zero_volatility.append(secid.name_secid)
            continue
        dict_volatility[secid.name_secid] = secid.volatility

    sort_keys = [i[0] for i in sorted(dict_volatility.items(), key=itemgetter(1), reverse=True)]
    max_volatility_keys = sort_keys[:3]
    min_volatility_keys = sort_keys[-3:]

    print('Максимальная волатильность:')
    for key in max_volatility_keys:
        print(f'{key} - {round(dict_volatility[key], 2):^5} %')

    print()

    print('Минимальная волатильность:')
    for key in min_volatility_keys:
        print(f'{key} - {round(dict_volatility[key], 2):^5} %')

    print()

    print('Нулевая волатильность:')
    zero_volatility.sort()
    print(', '.join(zero_volatility))

# TODO:
#  class КлассУправленец:
#  		def получить_набор_файлов()
#  		def запустить_исполнителей(кол_во_исполнителей=4)    # всех запустим последовательно, но в 02 уже параллельно
#  		def вывести данные
#  .
#  class КлассПарсер:
#  		def run()

if __name__ == '__main__':
    main()



