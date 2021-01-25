# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from operator import itemgetter


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
        self.statistics = defaultdict(int)

    def collect_statistics(self):
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                for symbol in line:
                    if symbol.isalpha():
                        self.statistics[symbol] += 1
        self.sort()
        self.print_statistics()

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

    def sort(self):
        pass


class SortAlphabetDown(LetterStatistics):
    def sort(self):
        self.sorted_keys = sorted(self.statistics.keys(), reverse=False)


class SortAlphabetUp(LetterStatistics):
    def sort(self):
        self.sorted_keys = sorted(self.statistics.keys(), reverse=True)


class SortResultDown(LetterStatistics):
    def sort(self):
        self.sorted_keys = [i[0] for i in sorted(self.statistics.items(), key=itemgetter(1), reverse=True)]


class SortResultUp(LetterStatistics):
    def sort(self):
        self.sorted_keys = [i[0] for i in sorted(self.statistics.items(), key=itemgetter(1), reverse=False)]


file_name = 'voyna-i-mir.txt'
# dict_sort = {
#     '1': SortAlphabetDown,
#     '2': SortAlphabetUp,
#     '3': SortResultDown,
#     '4': SortResultUp
# }

list_sort = [
    {'name': 'по алфавиту по возрастанию', 'class': SortAlphabetDown},
    {'name': 'по алфавиту по убыванию', 'class': SortAlphabetUp},
    {'name': 'по частоте по убыванию', 'class': SortResultDown},
    {'name': 'по частоте по возрастанию', 'class': SortResultUp},
]

while True:
    for i, elm in enumerate(list_sort):
        print(f'{i + 1} - {elm["name"]}')

    enter_sort = input('Как сортировать: ')
    if not enter_sort.isdigit():
        print('Используйте только цифры!')
        continue
    elif int(enter_sort) not in range(1, len(list_sort) + 1):
        print('Неверно введено значение!')
        continue

    list_sort[int(enter_sort) - 1]['class'](file_name=file_name).collect_statistics()
    # Но получается, что каждую итерацию цикла заново собирается статистика. Это получается медлеене, чем сначала
    # собрать статистику, а затем ее сортировать.

    stop = input('Закончить работу? ')
    if stop.lower() in ['да', 'yes']:
        break

# можно использовать defaultdict
#       from collections import defaultdict
#  .
#       s = 'mississippi'         # берем строку (итерируемый объект)
#       d = defaultdict(int)      # создаем словарь (подробности ниже)
#       for k in s:               # проходимся по строке и выполняем += 1 для каждой буквы.
#           d[k] += 1
#  .
#       print(d.items())          # [('i', 4), ('p', 2), ('s', 4), ('m', 1)]
#  .
#  Почему код выше работает? Почему на строке "d[k] += 1" при попытке обращение к незаданному ранее ключу
#  не происходит исключение?
#  .
#  Когда мы создаем словарь defaultdict, мы передаем ему ФУНКЦИЮ, которая будет вызываться для инициализации
#  значения, если это значение не найдено в словаре. Поэтому когда мы обращаемся print(d[1000500]) в словаре
#  будет создана пара ключ 1000500 и значение int() (т.е. 0, т.к. int() == 0)
#  .
#  Примеры:
#       d_1 = defaultdict(int)      # {}
#       d_1[100500] += 100          # {100500: 100}
#       x = d_1[123]                # x = 0, d={100500: 100, 123: 0}
#  .
#       d_2 = default(list)         # {}
#       x = d_2['hello']            # x = [], d={'hello': []}
#       d_2['test'].append(123)     # d={'hello': [], 'test': [123]}
#  .
#  Поэтому мы можем удалить проверку условия и смело обращаться к значению по ключу (даже если его еще
#  нет).

# Более "трушный" способ - вместо "lambda x: x[1]" использовать: itemgetter. А там где нельзя использовать
#  готовый метод/оператор мы будем писать lambda функции.
#  Пример:
#       # импортируем функцию, которая принимает индекс и выдает значение по нему, можно сказать
#       # что itemgetter - это и есть квадратные скобки '[]'
#       from operator import itemgetter
#       .
#       # .items() возвращает пары ключ-значение в виде кортежей. Поэтому здесь происходит сортировка
#       # списка пар ключ-значение. При этом в качестве ключа (критерия) кортировки берется значение,
#       # которое возвращает itemgetter для 1го (не 0го, а 1го) элемента. Т.е. для значения списка.
#       sorted(d.items(), key=itemgetter(1))

#  Какую цель мы преследуем?
#  Мы хотим реализовать поведенческий паттерн проектирования "Шаблонный метод"
#  в будущем (часть 2). Сначала прочтите описание этого простого шаблона по этой ссылке:
#       https://refactoring.guru/ru/design-patterns/template-method.
#  .
#  Какие будут шаги, что мы преследуем?
#  1. Сделать основной класс, который будет хранить весь алгоритм сбора данных с книги. Единственное, что не будет
#     делать этот класс - он не будет заниматься сортировкой. Его метод "сортировать" будет пустым и не будет
#     оказывать на собранные данные никакого эффекта. Хотя при этом, метод "сортировать" будет вызываться каждый раз
#     как только мы собрали данные (в конце метода "собрать данные");
#  2. Сделать классы-наследники. Несколько штук. Каждый из наследников перегружает только 1 метод. Какой?
#     Абсолютно верно - метод "сортировать".
#  .
#  В итоге у нас будет 1 родительский класс, который хранит весь алгоритм + N классов-наследников, которые
#  перегружая 1 метод "сортировать" будут корректировать работу основного алгоритма. Это и есть шаблонный метод)
#  .
#  Примечание: В шаблонном методе родитель может иметь больше 1 метода, которые надо перегрузить. Такой случай как
#  раз в задаче 03_files_arrange.py.

#  добавить подклассы и родительский класс
