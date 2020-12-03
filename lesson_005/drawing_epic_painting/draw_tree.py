# -*- coding: utf-8 -*-

import simple_draw as sd

COLOR_BROWN = (150, 75, 0)


def draw_tree(start_point, angle, length, width=10):
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

    draw_tree(start_point=v1_next_point, angle=v1_next_angle, length=next_length, width=next_width)
    draw_tree(start_point=v2_next_point, angle=v2_next_angle, length=next_length, width=next_width)
