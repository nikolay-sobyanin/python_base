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
    while quantity_corners > 1:
        v = sd.get_vector(start_point=start_point, angle=angle, length=length, width=3)
        v.draw(color=color)
        start_point = v.end_point
        angle += delta
        quantity_corners -= 1
    sd.line(start_point=start_point, end_point=point, color=color, width=3)


def draw_triangle(point, angle, length):
    n = 3  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_square(point, angle, length):
    n = 4  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_pentagon(point, angle, length):
    n = 5  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def draw_hexagon(point, angle, length):
    n = 6  # количество углов
    draw(point=point, angle=angle, length=length, quantity_corners=n, color=color)


def list_print(*args):
    print('Возможные цвета фигуры:')
    for i, arg in enumerate(args):
        print(f'{i}  :   {arg}')


all_color = {
    'red': sd.COLOR_RED,
    'orange': sd.COLOR_ORANGE,
    'yellow': sd.COLOR_YELLOW,
    'green': sd.COLOR_GREEN,
    'cyan': sd.COLOR_CYAN,
    'blue': sd.COLOR_BLUE,
    'purple': sd.COLOR_PURPLE,
}

list_color = list(all_color)
list_print(*list_color)

number_color = int(input('Введите номер цвета: '))

if 0 <= number_color <= len(list_color) - 1:
    color = all_color[list_color[number_color]]
else:
    print('Неккоректно введен номер цвета!')

point_0 = sd.get_point(150, 400)
draw_triangle(point=point_0, angle=0, length=100)

point_0 = sd.get_point(400, 400)
draw_square(point=point_0, angle=40, length=100)

point_0 = sd.get_point(400, 200)
draw_pentagon(point=point_0, angle=50, length=100)

point_0 = sd.get_point(200, 150)
draw_hexagon(point=point_0, angle=70, length=100)

sd.pause()
