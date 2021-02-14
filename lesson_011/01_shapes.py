# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    def draw(point, angle, length):
        start_point = point
        delta = 360 / n
        for i in range(0, n - 1):
            v = sd.get_vector(start_point=start_point, angle=angle + i * delta, length=length, width=3)
            v.draw()
            start_point = v.end_point
        sd.line(start_point=start_point, end_point=point, width=3)
    return draw


draw_triangle = get_polygon(n=3)
draw_triangle(point=sd.get_point(200, 200), angle=13, length=100)

draw_square = get_polygon(n=4)
draw_square(point=sd.get_point(500, 200), angle=45, length=100)


sd.pause()

# зачет!