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


sd.resolution = (1200, 600)
N = 40
list_snowflakes = []

for i in range(0, N):
    list_snowflakes.append({
        'x': sd.random_number(100, 1100),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    })

while not sd.user_want_exit():
    sd.start_drawing()
    # sd.clear_screen()
    for i, snowflakes in enumerate(list_snowflakes):
        point = sd.get_point(snowflakes['x'], snowflakes['y'])
        sd.snowflake(center=point, length=snowflakes['length'], color=sd.background_color)

    for i, snowflakes in enumerate(list_snowflakes):
        snowflakes['y'] -= 10
        snowflakes['x'] -= sd.random_number(-10, 10)

        new_point = sd.get_point(snowflakes['x'], snowflakes['y'])
        sd.snowflake(center=new_point, length=snowflakes['length'], color=sd.COLOR_WHITE)

        if snowflakes['y'] < 20:
            list_snowflakes.pop(i)
            list_snowflakes.append({
                'x': sd.random_number(100, 1100),
                'y': sd.random_number(400, 600),
                'length': sd.random_number(10, 25),
            })

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
