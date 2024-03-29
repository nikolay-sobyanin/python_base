#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Создайте списки:

# моя семья (минимум 3 элемента, есть еще дедушки и бабушки, если что)
my_family = ['mother', 'father', 'brother', 'grandmother']


# список списков приблизителного роста членов вашей семьи
my_family_height = [
    # ['имя', рост],
    [my_family[0], 175],
    [my_family[1], 180],
    [my_family[2], 184],
    [my_family[3], 170],
]

# Выведите на консоль рост отца в формате
#   Рост отца - ХХ см

print(f'Рост {my_family[1]} - {my_family_height[1][1]} см.')

# Выведите на консоль общий рост вашей семьи как сумму ростов всех членов
#   Общий рост моей семьи - ХХ см

all_height_my_family = my_family_height[0][1] + my_family_height[1][1] + my_family_height[2][1] + my_family_height[3][1]

print(f'Общий рост моей семьи - {all_height_my_family} см.')



#  Вы использовали str(), чтобы сложить строку (имя героя) и число (рост). Именно для вывода так делать не стоит. Можно,
#  если наша задача - получить строку, с которой мы будем дальше работать (искать по ней или ссылаться на нее), а просто
#  для вывода - плохая идея. Как быть?


# Рассмотрим 3 способа вывода и строки, и числа:
#  №1. Вывод через запятую.
#       name = 'Форрест Гамп'
#       age = 25
#       print('Мое имя — ', name, '. Люди зовут меня ', name, '. Мне ', age)        # просто через запятую перечисляем
#  .
#  №2. Вывод с использованием .format (это вы изучите в 6ом модуле).
#       print('Мое имя — {}. Люди зовут меня {}. Мне {}.'.format(name, name, age))  # вместо {} будут подставлены
#                                                                                   # переменные name, name, age.
#  .
#  №3. f-strings (или f-строки) (это вы тоже изучите в 6ом модуле)
#       print(f'Мое имя — {name}. Люди зовут меня {name}. Мне {age}.')
#  Строка начинается с f'' (поэтому и f-строки). В места, где нужно подставить переменную мы пишем: {<<имя переменной>>}
#  .
#  .
#  Выберите один из понравившихся вариантов и сделайте через него.
#  Самый быстрый (по скорости работы) и современный - f-строки, хотя ими не всегда можно пользоваться.
#  Рекомендую 2ой или 3ий.

# зачет!