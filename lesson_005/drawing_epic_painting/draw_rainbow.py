# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)

x_start_point = 50
x_end_point = 450
step = 25
for color in rainbow_colors:
    start_point = sd.get_point(x_start_point, 350)
    end_point = sd.get_point(x_end_point, 450)
    sd.line(start_point=start_point, end_point=end_point, color=color, width=4)
    x_start_point += step
    x_end_point += step
sd.sleep(seconds=3)

# Подсказка: цикл нужно делать сразу по тьюплу с цветами радуги.


# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво
center_point = sd.get_point(600, -300)
radius = 700
step_radius = 20
for color in rainbow_colors:
    sd.circle(center_position=center_point, radius=radius, color=color, width=step_radius)
    radius += step_radius

sd.pause()

# зачет!