# -*- coding: utf-8 -*-

import simple_draw as sd

WIDTH_CANVAS = 400
HEIGHT_CANVAS = 400

sd.resolution = (WIDTH_CANVAS, HEIGHT_CANVAS)

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


def draw(point, angle, length, quantity_corners, color=sd.COLOR_RED):
    start_point = point
    delta = 360 / quantity_corners
    for i in range(0, quantity_corners - 1):
        v = sd.get_vector(start_point=start_point, angle=angle + i * delta, length=length, width=3)
        v.draw(color=color)
        start_point = v.end_point
    sd.line(start_point=start_point, end_point=point, color=color, width=3)


def draw_triangle(point, angle, length):
    n = 3  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n)


def draw_square(point, angle, length):
    n = 4  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n)


def draw_pentagon(point, angle, length):
    n = 5  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n)


def draw_hexagon(point, angle, length):
    n = 6  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n)


def list_print(*args, key='name'):
    print('Возможные фигуры:')
    for i, arg in enumerate(args):
        print(f'{i}  :   {arg[key]}')


all_figure = (
    {
        'name': 'треугольник',
        'function': draw_triangle
    },
    {
        'name': 'квадрат',
        'function': draw_square
    },
    {
        'name': 'пятиугольник',
        'function': draw_pentagon
    },
    {
        'name': 'шестиугольник',
        'function': draw_hexagon
    },
)

list_print(*all_figure)
point_0 = sd.get_point(WIDTH_CANVAS / 2, HEIGHT_CANVAS / 2)
while True:
    number_figure = int(input('Введите номер цвета: '))
    # TODO:
    #  1. если заменить правый "<=" на "<", то можно будет убрать "- 1";
    #  2. давайте добавим проверку isdigit(), для того, чтобы защититься от ввода вида "привет123".
    #     Пример:
    #           print('123'.isdigit())          # True
    #           print('asdasda'.isdigit())      # False
    if 0 <= number_figure <= len(all_figure) - 1:
        select_figure = all_figure[number_figure]['function']
        select_figure(point=point_0, angle=10, length=100)
        break
    else:
        print('Неккоректно введен номер цвета!')


sd.pause()

# зачет!