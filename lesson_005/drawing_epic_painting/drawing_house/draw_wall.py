# -*- coding: utf-8 -*-
import simple_draw as sd

BRICK_LENGTH = 50
BRICK_HEIGHT = 25


def draw_wall(point_x, point_y, length, height):
    for row_number, y in enumerate(range(point_y, point_y + height, BRICK_HEIGHT)):
        step = 0 if row_number % 2 == 1 else BRICK_LENGTH // 2
        for x in range(point_x + step, point_x + length - BRICK_LENGTH + 1, BRICK_LENGTH):
            left_bottom = sd.get_point(x, y)
            right_top = sd.get_point(x + BRICK_LENGTH, y + BRICK_HEIGHT)
            sd.rectangle(left_bottom=left_bottom, right_top=right_top, color=(169, 169, 169), width=2)
