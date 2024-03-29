# -*- coding: utf-8 -*-

import simple_draw as sd

# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) Запустить вашу рекурсивную функцию, используя следующие параметры:
# root_point = sd.get_point(300, 30)
# draw_branches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения

# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()

COLOR_BROWN = (150, 75, 0)


def draw_branches(start_point, angle, length, width=10):
    color = COLOR_BROWN

    if length < 1:
        return

    if length < 10:
        color = sd.COLOR_GREEN

    v1 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=width)
    v1.draw(color=color)
    v2 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=width)
    v2.draw(color=color)

    v1_next_point = v1.end_point
    v2_next_point = v2.end_point
    v1_next_angle = angle + 30 * sd.random_number(60, 140) / 100
    v2_next_angle = angle - 30 * sd.random_number(60, 140) / 100
    next_length = length * .75 * sd.random_number(80, 120) / 100
    next_width = int(length * 0.1)

    draw_branches(start_point=v1_next_point, angle=v1_next_angle, length=next_length, width=next_width)
    draw_branches(start_point=v2_next_point, angle=v2_next_angle, length=next_length, width=next_width)


root_point = sd.get_point(300, 30)

# TODO: Добавил для ускорения
sd.start_drawing()
draw_branches(start_point=root_point, angle=90, length=100, width=12)
sd.finish_drawing()

sd.pause()

# зачет!