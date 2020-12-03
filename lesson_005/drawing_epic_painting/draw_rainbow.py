# -*- coding: utf-8 -*-

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)


def draw_rainbow(center_x, center_y, radius):
    center_point = sd.get_point(center_x, center_y)
    step_radius = 20
    for color in rainbow_colors:
        sd.circle(center_position=center_point, radius=radius, color=color, width=step_radius)
        radius += step_radius
