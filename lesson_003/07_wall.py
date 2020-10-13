# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

CANVAS_LENGTH = 1000
CANVAS_HEIGHT = 500

# TODO: как проверить, что все готово? Сделайте экран 800 на 600, а размер кирпича: длина=40, высота=20.
#  И сразу вопрос: почему стена покосилась? Надо сделать фикс, такой, чтобы при изменении параметров стены/кирпича
#  больше таких перекосов не было.
BRICK_LENGTH = 40
BRICK_HEIGHT = 20

sd.resolution = (CANVAS_LENGTH, CANVAS_HEIGHT)

for row_number, y in enumerate(range(0, CANVAS_HEIGHT + 1, BRICK_HEIGHT)):
    step = 0 if row_number % 2 == 1 else 50
    for x in range(step, CANVAS_LENGTH + 1, BRICK_LENGTH):
        left_bottom = sd.get_point(x, y)
        right_top = sd.get_point(x + BRICK_LENGTH, y + BRICK_HEIGHT)
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