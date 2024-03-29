# -*- coding: utf-8 -*-

# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)

import simple_draw as sd
from drawing_epic_painting.drawing_house.draw_house import draw_house
from drawing_epic_painting.draw_tree import draw_tree
from drawing_epic_painting.draw_snowfall import draw_snowfall
from drawing_epic_painting.draw_rainbow import draw_rainbow
from drawing_epic_painting.draw_cloud import draw_cloud
from drawing_epic_painting.draw_sun import draw_sun

# Небо
sd.resolution = (1200, 800)
sd.background_color = (135, 206, 235)
# Трава
sd.circle(center_position=sd.get_point(600, -3850), radius=4000, color=sd.COLOR_GREEN, width=0)
sd.start_drawing()
draw_house(point_x=500, point_y=100, length=300, height=200)
draw_cloud(center_x=200, center_y=700)
draw_tree(start_point=sd.get_point(1000, 50), angle=90, length=100, width=10)
sd.finish_drawing()

global_counter = 0
while not sd.user_want_exit():
    sd.start_drawing()

    draw_snowfall()
    draw_rainbow(point_rainbow=sd.get_point(1400, 1000), radius=400, color_offset=global_counter % 7)
    draw_sun(point_sun=sd.get_point(650, 700), ray_offset=global_counter)
    global_counter += 1

    sd.finish_drawing()
    sd.sleep(0.1)

sd.pause()

# зачет!