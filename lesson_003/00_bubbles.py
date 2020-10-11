# -*- coding: utf-8 -*-

import simple_draw as sd

# Размер окна для рисования
sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей

point_1 = sd.get_point(100, 500)
radius_1 = 20
for _ in range(3):
    radius_1 += 5
    sd.circle(center_position=point_1, radius=radius_1, color=sd.COLOR_WHITE, width=2)
sd.sleep(seconds=2)


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
def draw_a_bubble(point, radius, step, color, width):
    for _ in range(3):
        sd.circle(center_position=point, radius=radius, color=color, width=width)
        radius += step


# Нарисовать 10 пузырьков в ряд
quantity_draw_a_bubbles = 10
for x in range(100, (quantity_draw_a_bubbles * 100 + 1), 100):
    point_2 = sd.get_point(x, 400)
    draw_a_bubble(point=point_2, radius=20, step=5, color=sd.COLOR_RED, width=2)
sd.sleep(seconds=2)

# Нарисовать три ряда по 10 пузырьков
for y in range(100, (3 * 100 + 1), 100):
    for x in range(100, (quantity_draw_a_bubbles * 100 + 1), 100):
        point_3 = sd.get_point(x, y)
        draw_a_bubble(point=point_3, radius=20, step=5, color=sd.COLOR_GREEN, width=1)
sd.sleep(seconds=2)

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
for _ in range(100):
    random_point = sd.random_point()
    random_color = sd.random_color()
    random_radius = sd.randint(10, 21)
    draw_a_bubble(point=random_point, radius=random_radius, step=5, color=random_color, width=1)

sd.pause()

# TODO: можно просто draw_bubble (предлоги и союзы как правило опускают, как в телеграммах)

# зачет!