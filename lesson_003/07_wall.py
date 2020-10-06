# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for


sd.resolution = (1000, 800)
brick_length, brick_height = 100, 50
i = 1

for y in range(0, (sd.resolution[1] + 1), brick_height):
    if (i % 2) == 1:
        step = 0
    else:
        step = -50
    i += 1
    for x in range(0, (sd.resolution[0] + 1), brick_length):
        left_bottom = sd.get_point(x + step, y)
        right_top = sd.get_point((x + step + brick_length), (y + brick_height))
        sd.rectangle(left_bottom=left_bottom, right_top=right_top, color=sd.COLOR_DARK_ORANGE, width=1)

# Подсказки:
#  Для отрисовки кирпича использовать функцию rectangle
#  Алгоритм должен получиться приблизительно такой:
#
#   цикл по координате Y
#       вычисляем сдвиг ряда кирпичей
#       цикл координате X
#           вычисляем правый нижний и левый верхний углы кирпича
#           рисуем кирпич

sd.pause()
