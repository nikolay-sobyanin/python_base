# -*- coding: utf-8 -*-

import os

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

# После зачета первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию


class LetterStatistics:

    def __init__(self, file_name):
        self.file_name = file_name
        self.sorted_keys = []
        self.statistics = {}

    def collect_statistics(self):
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                for symbol in line:
                    self.count_letter(symbol)
        self.sorted_keys = self.statistics.keys()

    def count_letter(self, symbol):
        if symbol.isalpha():
            if symbol in self.statistics:
                self.statistics[symbol] += 1
            else:
                self.statistics[symbol] = 1

    def print_statistics(self):
        total_letters = sum(self.statistics.values())
        column_width = 15
        print(f'+{"":-^{column_width}}+{"":-^{column_width}}+')
        print(f'|{"Буква":^{column_width}}|{"Частота":^{column_width}}|')
        print(f'+{"":-^{column_width}}+{"":-^{column_width}}+')
        for i in self.sorted_keys:
            print(f'|{i:^{column_width}}|{self.statistics[i]:^{column_width}}|')
            print(f'+{"":-^{column_width}}+{"":-^{column_width}}+')
        print(f'|{"Итого":^{column_width}}|{total_letters:^{column_width}}|')
        print(f'+{"":-^{column_width}}+{"":-^{column_width}}+')

    def sort_alphabet(self, reverse=False):
        self.sorted_keys = sorted(self.statistics.keys(), reverse=reverse)

    def sort_result(self, reverse=True):
        self.sorted_keys = [i[0] for i in sorted(list(self.statistics.items()), key=lambda x: x[1], reverse=reverse)]


text = LetterStatistics(file_name='voyna-i-mir.txt')
text.collect_statistics()

while True:
    print('Сортировать статистику:')
    print('1 - по алфавиту по возрастанию')
    print('2 - по алфавиту по убыванию')
    print('3 - по частоте по убыванию')
    print('4 - по частоте по возрастанию')
    enter_sort = int(input('Как сортировать: '))
    if enter_sort not in [1, 2, 3, 4]:
        print('Неверно введено значение!')
        continue
    if enter_sort == 1:
        text.sort_alphabet()
    elif enter_sort == 2:
        text.sort_alphabet(reverse=True)
    elif enter_sort == 3:
        text.sort_result()
    else:
        text.sort_result(reverse=False)
    text.print_statistics()

    stop = input('Закончить работу? ')
    if stop.lower() in ['да', 'yes']:
        break
