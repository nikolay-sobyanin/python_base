# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())

# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава


class Water:

    def __init__(self):
        self.name = 'Вода'

    def __str__(self):
        return self.name

    def __add__(self, other):
        # TODO: создавать объекты, чтобы сравнить с их именами - ну такое.
        # TODO: Используйте isinstance(), чтобы определить класс элемента.
        #  .
        #         class A (list):
        #            pass
        #  .
        #         a = A()
        #         isinstance(a,A)             # True
        #         isinstance(a,list)          # True
        #         isinstance(a,dict)          # False
        #  .
        if other.name == Air().name:
            return Storm()
        elif other.name == Fire().name:
            return Vapor()
        elif other.name == Ground().name:
            return Mud()
        else:
            return None


class Air:

    def __init__(self):
        self.name = 'Воздух'

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.name == Fire().name:
            return Lightning()
        elif other.name == Ground().name:
            return Dust()
        elif other.name == Water().name:
            return Storm()
        else:
            return None


class Fire:

    def __init__(self):
        self.name = 'Огонь'

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.name == Ground().name:
            return Lava()
        elif other.name == Air().name:
            return Lightning()
        elif other.name == Water().name:
            return Vapor()
        else:
            return None


class Ground:

    def __init__(self):
        self.name = 'Земля'

    def __str__(self):
        return self.name


class Storm:

    def __init__(self):
        self.name = 'Шторм'

    def __str__(self):
        return self.name


class Vapor:

    def __init__(self):
        self.name = 'Пар'

    def __str__(self):
        return self.name


class Mud:

    def __init__(self):
        self.name = 'Грязь'

    def __str__(self):
        return self.name


class Lightning:

    def __init__(self):
        self.name = 'Молния'

    def __str__(self):
        return self.name


class Dust:

    def __init__(self):
        self.name = 'Пыль'

    def __str__(self):
        return self.name


class Lava:

    def __init__(self):
        self.name = 'Лава'

    def __str__(self):
        return self.name



# TODO: Добавьте цикл.
#  Создайте список из всех элементов и пройдитесь по нему в 2х циклах, т.о. мы сможем получить разнообразные комбинации
#  всех элементов. Сделайте цикл так, чтобы пар-дублей (вода-огонь, огонь-вода) не было. Для этого пригодится
#  enumerate()


# TODO: сделайте так, чтобы не было повторных пересечений. Например:
#       Вода + Огонь = Пар
#       Огонь + Вода = Пар (эта пара лишняя, т.к. от перестановки мест слагаемых сумма не меняется)
#  .
#  Как это лучше сделать?
#  Дам 2 наводки:
#   1. используйте enumerate() для 1го цикла;
#   2. Для второго цикл используйте не весь element_list, а только его срез начиная какого элемента.
#  .
#  Пример:
#  Пусть у нас есть список [1,2,3,4], сейчас мы имеем 16 пар: 1-1,1-2,1-3,...2-1,...,3-1, ...;
#  А хотим иметь только уникальные пары:
#  1-1, 1-2, 1-3, 1-4
#       2-2, 2-3, 2-4
#            3-3, 3-4
#                 4-4
#  .
print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Fire(), '=', Water() + Fire())
print(Water(), '+', Ground(), '=', Water() + Ground())
print(Air(), '+', Fire(), '=', Air() + Fire())
print(Air(), '+', Ground(), '=', Air() + Ground())
print(Fire(), '+', Ground(), '=', Fire() + Ground())

print(Air(), '+', Water(), '=', Air() + Water())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
