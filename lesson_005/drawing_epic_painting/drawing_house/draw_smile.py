# -*- coding: utf-8 -*-
import simple_draw as sd


# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_smile(x, y):
    # Элипс
    left_bottom_ellipse = sd.get_point(x - 35, y - 30)
    right_top_ellipse = sd.get_point(x + 35, y + 30)
    sd.ellipse(left_bottom=left_bottom_ellipse, right_top=right_top_ellipse, color=sd.COLOR_YELLOW, width=0)
    # Рот
    points_of_mouth = [
        sd.get_point(x - 15, y - 5),
        sd.get_point(x - 8, y - 10),
        sd.get_point(x + 8, y - 10),
        sd.get_point(x + 15, y - 5)
    ]
    sd.lines(point_list=points_of_mouth, color=sd.COLOR_BLACK, closed=False, width=2)
    # Глаза
    eye_radius = 6
    center_point_1 = sd.get_point(x + 12, y + 12)
    center_point_2 = sd.get_point(x - 12, y + 12)
    sd.circle(center_position=center_point_1, radius=eye_radius, color=sd.COLOR_BLACK, width=2)
    sd.circle(center_position=center_point_2, radius=eye_radius, color=sd.COLOR_BLACK, width=2)
