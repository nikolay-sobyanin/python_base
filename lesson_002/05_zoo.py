#!/usr/bin/env python
# -*- coding: utf-8 -*-

# есть список животных в зоопарке

zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]

# посадите медведя (bear) между львом и кенгуру
#  и выведите список на консоль

zoo.insert(1, 'bear')
print(zoo)

# добавьте птиц из списка birds в последние клетки зоопарка
birds = ['rooster', 'ostrich', 'lark', ]
#  и выведите список на консоль

zoo.extend(birds)
print(zoo)

# уберите слона
#  и выведите список на консоль

zoo.remove('elephant')
print(zoo)

# выведите на консоль в какой клетке сидит лев (lion) и жаворонок (lark).
# Номера при выводе должны быть понятны простому человеку, не программисту.

serial_number_lion = zoo.index('lion') + 1
serial_number_lark = zoo.index('lark') + 1

print('Порядковый номер льва - ' + str(serial_number_lion))
print('Порядковый номер жаворонка - ' + str(serial_number_lark))


