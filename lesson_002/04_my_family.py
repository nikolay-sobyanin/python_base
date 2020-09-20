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

print('Рост ' + my_family[1] + ' - ' + str(my_family_height[1][1]) + ' см')

# Выведите на консоль общий рост вашей семьи как сумму ростов всех членов
#   Общий рост моей семьи - ХХ см

all_height_my_family = my_family_height[0][1] + my_family_height[1][1] + my_family_height[2][1] + my_family_height[3][1]

print('Общий рост моей семьи - ' + str(all_height_my_family) + ' см')