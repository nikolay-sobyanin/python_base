# -*- coding: utf-8 -*-

import simple_draw as sd


# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


def get_snowflake():
    return {
        'x': sd.random_number(100, 1100),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    }


sd.resolution = (1200, 600)
N = 40
list_snowflakes = []

for _ in range(0, N):
    list_snowflakes.append(get_snowflake())

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

        if snowflake['y'] < 20:
            snowflake.update(get_snowflake())

    sd.finish_drawing()
    sd.sleep(0.1)

sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg

# зачет!