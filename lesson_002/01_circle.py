#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть значение радиуса круга
radius = 42

# Выведите на консоль значение прощади этого круга с точностю до 4-х знаков после запятой
# подсказки:
#       формулу можно подсмотреть в интернете,
#       пи возьмите равным 3.1415926
#       точность указывается в функции round()

# TODO: С точки зрения результата - все правильно.
#  +5 к карме за создание переменной pi. Это правильный стиль! При работе со сложными формулами лучше именовать
#  константы (например: "pi" вместо 3.14 и "e" вместо 2.72), это сильно повышает читабельность кода, и позволяет
#  изменять значение константы в одном месте, а не выискивать ее по коду через Ctrl+F. Как вы и сделали. Отлично!
#  .
#  Вы можете улучшить свой код, заменив собственную переменную pi на переменную pi из модуля math. Этим модулем
#  полезно пользоваться при работе с математическими функциями (sin, cos и т.п.) и константами (Пи, число е). Пример:
#       import math
#                                                   # между импортом модулей и ост. кодом есть пустая строка. Это стиль)
#       circle_length = 2 * math.pi * radius        # Пример рассчета длины окружности
#  .
#  p.s. импортирование модулей всегда производится выше всех останых строк кода (даже выше radius), в данном случае на
#       3 строчке, т.к. первые две строки - специальный комментарии подсказывающие кодировку файла и путь к
#       Интерпретатору.
pi = 3.1415926
area_circle = pi * radius ** 2
area_circle = round(area_circle, 4)
print(area_circle)


# Далее, пусть есть координаты точки
point_1 = (23, 34)
# где 23 - координата х, 34 - координата у

# Если точка point лежит внутри того самого круга [центр в начале координат (0, 0), radius = 42],
# то выведите на консоль True, Или False, если точка лежит вовне круга.
# подсказки:
#       нужно определить расстояние от этой точки до начала координат (0, 0)
#       формула так же есть в интернете
#       квадратный корень - это возведение в степень 0.5
#       операции сравнения дают булевы константы True и False

distance_point_1 = (point_1[0] ** 2 + point_1[1] ** 2) ** 0.5

print(distance_point_1 < radius)

# Аналогично для другой точки
point_2 = (30, 30)
# Если точка point_2 лежит внутри круга (radius = 42), то выведите на консоль True,
# Или False, если точка лежит вовне круга.

distance_point_2 = (point_2[0] ** 2 + point_2[1] ** 2) ** 0.5
print(distance_point_2 < radius)

# Пример вывода на консоль:
#
# 77777.7777
# False
# False


