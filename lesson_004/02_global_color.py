# -*- coding: utf-8 -*-
import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg


def draw(point, angle, length, quantity_corners, color):
    start_point = point
    delta = 360 / quantity_corners
    for i in range(0, quantity_corners - 1):
        v = sd.get_vector(start_point=start_point, angle=angle + i * delta, length=length, width=3)
        v.draw(color=color)
        start_point = v.end_point
    sd.line(start_point=start_point, end_point=point, color=color, width=3)


def draw_triangle(point, angle, length, color):
    n = 3  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_square(point, angle, length, color):
    n = 4  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_pentagon(point, angle, length, color):
    n = 5  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_hexagon(point, angle, length, color):
    n = 6  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def list_print(*args, key='name'):
    print('Возможные цвета фигуры:')
    for i, arg in enumerate(args):
        print(f'{i}  :   {arg[key]}')


# all_color = {
#     'red': sd.COLOR_RED,
#     'orange': sd.COLOR_ORANGE,
#     'yellow': sd.COLOR_YELLOW,
#     'green': sd.COLOR_GREEN,
#     'cyan': sd.COLOR_CYAN,
#     'blue': sd.COLOR_BLUE,
#     'purple': sd.COLOR_PURPLE,
# }

all_color = (
    {
        'name': 'red',
        'color': sd.COLOR_RED
    },
    {
        'name': 'orange',
        'color': sd.COLOR_ORANGE
    },
    {
        'name': 'yellow',
        'color': sd.COLOR_YELLOW
    },
    {
        'name': 'green',
        'color': sd.COLOR_GREEN
    },
    {
        'name': 'cyan',
        'color': sd.COLOR_CYAN
    },
    {
        'name': 'blue',
        'color': sd.COLOR_BLUE
    },
    {
        'name': 'purple',
        'color': sd.COLOR_PURPLE
    },
)

list_print(*all_color)

while True:
    number_color = int(input('Введите номер цвета: '))
    if 0 <= number_color <= len(all_color) - 1:
        select_color = all_color[number_color]['color']
        break
    else:
        print('Неккоректно введен номер цвета!')

point_0 = sd.get_point(150, 400)
draw_triangle(point=point_0, angle=0, length=100, color=select_color)

point_0 = sd.get_point(400, 400)
draw_square(point=point_0, angle=40, length=100, color=select_color)

point_0 = sd.get_point(400, 200)
draw_pentagon(point=point_0, angle=50, length=100, color=select_color)

point_0 = sd.get_point(200, 150)
draw_hexagon(point=point_0, angle=70, length=100, color=select_color)

sd.pause()
