# -*- coding: utf-8 -*-

import simple_draw as sd

rainbow_colors = [sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE]


def draw_rainbow(point_rainbow, radius, color_offset):
    new_colors = rainbow_colors[color_offset:] + rainbow_colors[:color_offset]
    step_radius = 20
    for color in new_colors:
        sd.circle(center_position=point_rainbow, radius=radius, color=color, width=step_radius)
        radius += step_radius
