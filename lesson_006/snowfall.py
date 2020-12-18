# -*- coding: utf-8 -*-

import simple_draw as sd

list_snowflakes = []


def get_snowflake():
    return {
        'x': sd.random_number(100, 1100),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    }


def create_snowflakes(N=40):
    global list_snowflakes
    for _ in range(0, N):
        list_snowflakes.append(get_snowflake())


def draw_snowflakes(color):
    for snowflake in list_snowflakes:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(center=point, length=snowflake['length'], color=color)


def shifting_snowflakes():
    for snowflake in list_snowflakes:
        snowflake['y'] -= 10
        snowflake['x'] -= sd.random_number(-10, 10)


def new_snowflake():
    for snowflake in list_snowflakes:
        if snowflake['y'] < 20:
            snowflake.update(get_snowflake())
