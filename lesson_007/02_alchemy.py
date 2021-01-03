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
        if isinstance(other, Air):
            return Storm()
        elif isinstance(other, Fire):
            return Vapor()
        elif isinstance(other, Ground):
            return Mud()
        else:
            return None


class Air:

    def __init__(self):
        self.name = 'Воздух'

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Fire):
            return Lightning()
        elif isinstance(other, Ground):
            return Dust()
        elif isinstance(other, Water):
            return Storm()
        else:
            return None


class Fire:

    def __init__(self):
        self.name = 'Огонь'

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Ground):
            return Lava()
        elif isinstance(other, Air):
            return Lightning()
        elif isinstance(other, Water):
            return Vapor()
        else:
            return None


class Ground:

    def __init__(self):
        self.name = 'Земля'

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Fire):
            return Lava()
        elif isinstance(other, Air):
            return Dust()
        elif isinstance(other, Water):
            return Mud()
        else:
            return None


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


element_list = [Water(), Air(), Fire(), Ground()]

for i, element_1 in enumerate(element_list):
    for element_2 in element_list[i:]:
        print(element_1, '+', element_2, '=', element_1 + element_2)

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
