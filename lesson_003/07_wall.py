# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for


sd.resolution = (1000, 800)
# TODO: создайте константы ШИРИНА и ВЫСОТА экрана.
BRICK_LENGTH = 100      # <== стиль констант.
brick_height = 50

# TODO: используйте enumerate(), чтобы быстро и удобно получить номер ряда. (пример внизу)
i = 1
for y in range(0, (sd.resolution[1] + 1), brick_height):        # <== используйте созданную константу ВЫСОТА_ПОЛОТНА
    # TODO: дополнительно. Если if|else нужен только для того, чтобы прибавить/отнять какое-то число от исходного, то
    #  можно использовать тернальный оператор if|else. Пример:
    #               if some_condition:
    #                   a = 100
    #               else:                       			 # было
    #                   a = 200.
    #  .
    #               a = 100 if some_condition else 200       # стало
    #  .              ↑  ↑                          ↑
    #  Аналогично и +=, *=, -=, /=:
    #               a *= 4 if some_condition_2 else 2        # если ДА - умножим в 4 раза, если НЕТ - в 2 раза
    #  .               ↑ ↑                          ↑
    if (i % 2) == 1:    # TODO: скобки можно убрать
        step = 0
    else:
        step = -50
    i += 1

    # TODO: вместо 0 стоит подставить "отступ", посчитанный в условии выше.
    for x in range(0, (sd.resolution[0] + 1), BRICK_LENGTH):
        # TODO: Тогда тут можно будет убрать  " + step" в обоих строках.
        left_bottom = sd.get_point(x + step, y)
        right_top = sd.get_point((x + step + BRICK_LENGTH), (y + brick_height))
        sd.rectangle(left_bottom=left_bottom, right_top=right_top, color=sd.COLOR_DARK_ORANGE, width=1)

# TODO: Пример "enumerate()":
#       seasons = ['Spring', 'Summer', 'Fall', 'Winter']
#       for season_id, season_name in enumerate(seasons):
# 	        print(season_id, ' - ', season_name)
#   .
#   В результате будет выведено:
#       0 - 'Spring'
#       1 - 'Summer'
#       2 - 'Fall'
#       3 - 'Winter'

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
