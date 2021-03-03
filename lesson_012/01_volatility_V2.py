import os
from operator import itemgetter
from library.utils import time_track


class SecidVolatility:

    def __init__(self, file_path):
        self.file_path = file_path
        self.name_secid = None
        self.volatility = None

    def parser_line(self, line):
        line = line.rstrip()
        secid, tradetime, full_price, quantity = line.split(',')
        price = float(full_price) / int(quantity)
        return secid, price

    def run(self):
        with open(self.file_path, 'r', encoding='utf8') as file:
            file.readline()
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


max_volatility = {}
min_volatility = {}
zero_volatility = []

dir_path = 'trades'
dir_path = os.path.normpath(dir_path)


@time_track
def main():
    secides = [SecidVolatility(file_path=file_path) for file_path in file_paths(dir_path=dir_path)]
    for secid in secides:
        secid.run()
        if secid.volatility == 0:
            zero_volatility.append(secid.name_secid)
            continue

        if len(max_volatility) < 3:
            max_volatility[secid.name_secid] = secid.volatility
            min_volatility[secid.name_secid] = secid.volatility
            continue

        for key, value in max_volatility.items():
            if secid.volatility > value:
                max_volatility.pop(key)
                max_volatility[secid.name_secid] = secid.volatility
                break

        for key, value in min_volatility.items():
            if secid.volatility < value:
                min_volatility.pop(key)
                min_volatility[secid.name_secid] = secid.volatility
                break

    max_sort_keys = [i[0] for i in sorted(max_volatility.items(), key=itemgetter(1), reverse=True)]
    min_sort_keys = [i[0] for i in sorted(min_volatility.items(), key=itemgetter(1), reverse=True)]

    print('Максимальная волатильность:')
    for key in max_sort_keys:
        print(f'{key} - {round(max_volatility[key], 2):^5} %')

    print()

    print('Минимальная волатильность:')
    for key in min_sort_keys:
        print(f'{key} - {round(min_volatility[key], 2):^5} %')

    print()

    print('Нулевая волатильность:')
    zero_volatility.sort()
    print(', '.join(zero_volatility))


if __name__ == '__main__':
    main()

# зачет!