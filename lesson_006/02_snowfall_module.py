# -*- coding: utf-8 -*-

import simple_draw as sd
import snowfall

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
# снежинки хранить в глобальных переменных модуля snowfall
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

sd.resolution = (1200, 600)

snowfall.create_snowflakes(N=100)
while not sd.user_want_exit():
    sd.start_drawing()
    snowfall.draw_snowflakes(color=sd.background_color)
    snowfall.shifting_snowflakes()
    snowfall.draw_snowflakes(color=sd.COLOR_WHITE)
    numbers_del_snowflakes = snowfall.numbers_reached_bottom_screen()
    snowfall.del_snowflakes(numbers=numbers_del_snowflakes)
    snowfall.create_snowflakes(N=len(numbers_del_snowflakes))
    sd.finish_drawing()
    sd.sleep(0.1)

sd.pause()

# зачет!