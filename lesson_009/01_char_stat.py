# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
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


class LetterStatistics(ABC):
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

    def print_statistics(self):
        self.collect_statistics()
        total_letters = sum(self.statistics.values())
        column_width = 15
        line = 2 * f'+{"":-^{column_width}}' + '+'
        print(line)
        print(f'|{"Буква":^{column_width}}|{"Частота":^{column_width}}|')
        print(line)
        for i in self.sorted_keys:
            print(f'|{i:^{column_width}}|{self.statistics[i]:^{column_width}}|')
            print(line)
        print(f'|{"Итого":^{column_width}}|{total_letters:^{column_width}}|')
        print(line)

    @abstractmethod
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
list_sort = [
    {'name': 'по алфавиту по возрастанию', 'class': SortAlphabetDown},
    {'name': 'по алфавиту по убыванию', 'class': SortAlphabetUp},
    {'name': 'по частоте по убыванию', 'class': SortResultDown},
    {'name': 'по частоте по возрастанию', 'class': SortResultUp},
]

# LetterStatistics(file_name=file_name).print_statistics()

while True:
    for i, elm in enumerate(list_sort, 1):
        print(f'{i} - {elm["name"]}')

    enter_sort = input('Как сортировать: ')
    if not enter_sort.isdigit():
        print('Используйте только цифры!')
        continue
    if not 1 <= int(enter_sort) <= len(list_sort):
        print('Неверно введено значение!')
        continue

    list_sort[int(enter_sort) - 1]['class'](file_name=file_name).print_statistics()

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

# исправлять не нужно, но немного надо озвучить:
#  сейчас сортировка сделана через список отсортированных ключей. А можно напрямую через .items().
#  Схема могла быть такая:
#   1. self.sort() возвращает отсортированные данные:
#          return sorted(self.statistics.items(), key=itemgetter(1), reverse=True)
#   2. а где вызывается sort? он вызывается либо внутри print_statistics:
#          for letter, amount in self.sort():
#             ....
#   .
#   .
#   Менять не нужно! Это для ознакомления. Мы используем себе на пользу наличие поля "self.sorted_keys".

    # Сейчас алгоритм работы такой: пользователь вводит данные как надо отсортировать информацию, собираем статистику, сортируем статистику, печатаем. Все выполняется по шаблону.
    # Но куда лучше след алгоритм: собрать статистику (записать ее в буфер), пользователь вводит как ему отсортировать ее, сортируем, печатаем.
    # Если нужна будет другая сортировка статистики уже не нужно будет заново считывать файл и собирать статистику.
    # Сейчас код быстро работает, а если бы был файл больше по объему.

    #  вынесите print_statistics из collect_statistics.
    #  Используем тот факт, что есть поле, хранящее отсортированные данные, здесь будем вызывать только print`ы.

    # Я вынесу print_statistics. Но поле хранящее отсортированные данные будет снова и снова формироваться каждую итерацию цикла.

    # Паттерн "шаблонный метод" ну логично действие выполняется по шаблону, но в данной конкретной задаче, применение данного метода, как я понял ни есть оптимально.
    # Ну либо я не правильно его применил в данной задачи, либо я overthinking снова.

    #  почему сделано именно так, и почему мы парсинг данных повторяется?
    #  Шаблонный метод применяют тогда, когда нужно создать "новый вид", но немного другой.
    #  Шаблонный метод - это способ избежать дублирования кода.
    #  .
    #  Его можно использовать в связке с паттерном Стратегия.
    #  Когда есть какой-то класс-менеджер, который делает какую-то свою задачу. Этот менеджер - большой класс, который
    #  использует созданные нами классы для парсинга файлов. Этот менеджер понятия не имеет какой именно класс он
    #  использует, ему только известно, что это будет наследник LetterStatistics. И исходя из этого он знает, что
    #  это объекта будет метод sort() и другие.
    #  .
    #  Как эту это пригождается?
    #  При создании Менеджера() мы ему передаем объект SortResultDown() или SortAlphabetUp() или еще какой. Пример:

    # class Manager:
    #     def __init__(self, sort_type):
    #         self.cur_parsing: LetterStatistics = sort_type
    #
    #     def sort(self):
    #         self.cur_parsing.sort()
    #
    #
    # Manager(sort_type=SortResultDown(file_name))
    # Manager(sort_type=SortAlphabetUp(file_name))

    #  при запуске программы, при инициализации Менеджера, тип сортировки, как правило, берут из конфига, в котором
    #  указано какой из методов использовать.
    #  .
    #  Профит: код Менеджера НИКАК ничего не знает о том, как именно он сортирует. Мы можем добавить 100500 видов
    #  парсинга и сортировки, лишь бы он соответствовал интерфейсу LetterStatistics, чтобы Менеджер знал, что ожидать.

# немного доп. инфы: имя класса можно достатать так:
#  SortAlphabetDown.__name__

#  Абстрактные базовые классы.
#  Немного доп.инфы. У нас есть Родительский класс и классы Наследники.
#  .
#  Сам класс Родитель будет не жизнеспособен (он - хранитель алгоритма, а детали реализации хранятся в детях):
#  т.е. если мы создадим объект этого класса, то он нам ничего отсортировать
#  не сможет, т.к. его метод сортировки - заглушка. При этом создать объект мы можем.
#  .
#  Как недопустить того, чтобы кто-то случайно не создал объект этого класса? Сделать класс абстрактным.
#  Абстракный класс - это класс, который имеет хотя бы 1 абстрактный метод. Что такое абстрактным метод?
#  Это метод, который имеет название, но не имеет реализации.
#  .
#  Если класс абстрактный, то создать объект этого класса не представляется возможным. Будет ошибка.
#  .
#  Зачем тогда нужны абстрактные классы?
#  Именно для таких случаев как наш: у нас есть класс-родитель, у которого объявлен метод, но реализации этого метода
#  нет. Классы наследники наследуя этот класс родитель перегружают его метод и по факту дают ему реализацию.
#  .
#  Пример:

# from abc import ABC, abstractmethod

# это абстрактный класс, он наследует от ABC (AbstractBaseClass)
# class MyAbstractBaseClass(ABC):
#     # принимает 2 аргумента
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     # этот декоратор показывает, что данные метод абстрактный. И при наследовании его обязательно нужно перегрузить.
#     @abstractmethod
#     def action(self):
#         pass
#
#     # метод который использует action() и возвращает результат
#     def get_result(self):
#         return self.action()
#
# # Класс-наследник, реализующий Сумму
# class SumClass(MyAbstractBaseClass):
#     # действие - сумма
#     def action(self):
#         return self.x + self.y
#
# # Класс-наследник, реализующий Произведение
# class MulClass(MyAbstractBaseClass):
#     # действие - произведение
#     def action(self):
#         return self.x * self.y

# Попытка создать объект Абстрактного Класса приведет к ошибке:
# "TypeError: Can't instantiate abstract class MyAbstractBaseClass with abstract methods action"
# MyAbstractBaseClass(x=100, y=500)   # ошибка

# Создаем объекты наследников
# object_sum = SumClass(x=100, y=500)
# print(object_sum.get_result())          # 600
#
# object_mul = MulClass(x=100, y=500)
# print(object_mul.get_result())          # 50000
#
#  задача: применить АБС внутри своего шаблона.
#  Примечание: у нас будет родительский абстрактный класс + 4 класса наследника.

# зачет!