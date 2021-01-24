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
                    # TODO: стоит совместить эту функцию и count_letter (TOD0 ниже все упростит)
                    self.count_letter(symbol)
        self.sorted_keys = self.statistics.keys()

    def count_letter(self, symbol):
        if symbol.isalpha():
            # TODO: Тут поможет defaultdict (см. чуть ниже)
            if symbol in self.statistics:
                self.statistics[symbol] += 1
            else:
                self.statistics[symbol] = 1

    # TODO: можно использовать defaultdict
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
        # TODO: Более "трушный" способ - вместо "lambda x: x[1]" использовать: itemgetter. А там где нельзя использовать
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


text = LetterStatistics(file_name='voyna-i-mir.txt')
text.collect_statistics()

# TODO: Какую цель мы преследуем?
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

# TODO: добавить подклассы и родительский класс

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
