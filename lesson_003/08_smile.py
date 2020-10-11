# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd


# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_a_smile(x, y, color):
    # Элипс
    left_bottom_ellipse = sd.get_point(x - 50, y - 40)
    right_top_ellipse = sd.get_point(x + 50, y + 40)
    sd.ellipse(left_bottom=left_bottom_ellipse, right_top=right_top_ellipse, color=color, width=1)
    # Рот
    point_1 = sd.get_point(x - 20, y - 10)
    point_2 = sd.get_point(x - 10, y - 15)
    point_3 = sd.get_point(x + 10, y - 15)
    point_4 = sd.get_point(x + 20, y - 10)
    points_of_mouth = [point_1, point_2, point_3, point_4]
    sd.lines(point_list=points_of_mouth, color=sd.COLOR_DARK_YELLOW, closed=False, width=3)
    # Глаза
    eye_radius = 6
    center_point_1 = sd.get_point(x + 15, y + 15)
    center_point_2 = sd.get_point(x - 15, y + 15)
    sd.circle(center_position=center_point_1, radius=eye_radius, color=color, width=1)
    sd.circle(center_position=center_point_2, radius=eye_radius, color=color, width=1)


for _ in range(10):
    x = sd.random_number(50, sd.resolution[0] - 50)
    y = sd.random_number(50, sd.resolution[1] - 50)
    draw_a_smile(x=x, y=y, color=sd.COLOR_YELLOW)

sd.pause()

# почти да
