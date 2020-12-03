# -*- coding: utf-8 -*-

import simple_draw as sd


def get_snowflake():
    return {
        'x': sd.random_number(10, 350),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    }


N = 40
list_snowflakes = []

for _ in range(0, N):
    list_snowflakes.append(get_snowflake())


def draw_snowfall():
    while not sd.user_want_exit():
        sd.start_drawing()

        for snowflake in list_snowflakes:
            point = sd.get_point(snowflake['x'], snowflake['y'])
            sd.snowflake(center=point, length=snowflake['length'], color=sd.background_color)

        for snowflake in list_snowflakes:
            snowflake['y'] -= 10
            snowflake['x'] -= sd.random_number(-10, 10)

            new_point = sd.get_point(snowflake['x'], snowflake['y'])
            sd.snowflake(center=new_point, length=snowflake['length'], color=sd.COLOR_WHITE)

            if snowflake['y'] < 150:
                snowflake.update(get_snowflake())

        sd.finish_drawing()
        sd.sleep(0.1)
