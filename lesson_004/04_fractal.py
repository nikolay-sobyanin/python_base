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


def draw_branches(start_point, angle, length):
    if length < 5:
        return
    # TODO: давайте немного усложним:
    #  Если длина ветки большая (сами решите), то красим коричневым.
    #  Если длина маленькая - зеленым.
    #  Добавить уменьшение ширины (пропорционально длине).
    #  .
    #  Что получится по итогу:
    #  Ветвистое дерево, у которого есть толстый ствол, ветки и мелкая листва.
    v1 = sd.get_vector(start_point=start_point, angle=angle, length=length)
    v1.draw(color=sd.COLOR_GREEN)
    v2 = sd.get_vector(start_point=start_point, angle=angle, length=length)
    v2.draw(color=sd.COLOR_GREEN)
    v1_next_point = v1.end_point
    v2_next_point = v2.end_point
    v1_next_angle = angle + 30 * sd.random_number(60, 140) / 100
    v2_next_angle = angle - 30 * sd.random_number(60, 140) / 100
    next_length = length * .75 * sd.random_number(80, 120) / 100
    draw_branches(start_point=v1_next_point, angle=v1_next_angle, length=next_length)
    draw_branches(start_point=v2_next_point, angle=v2_next_angle, length=next_length)


root_point = sd.get_point(300, 30)
draw_branches(start_point=root_point, angle=90, length=100)


sd.pause()


