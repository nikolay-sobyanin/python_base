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


def add_element_to_list(element, list_to_add=None):
    """добавляем элемент к списку"""
    if list_to_add is None:
        list_to_add = []
    list_to_add.append(element)
    return list_to_add


def draw_snowflake(*args):
    for i, arg in enumerate(args):
        point_0 = sd.get_point(arg[0], arg[1])
        sd.snowflake(center=point_0, length=arg[2])


N = 20

x_list = []
y_list = []
length_list = []

for i in range(0, N):
    _x_ = sd.random_number(100, 500)
    _y_ = sd.random_number(500, 600)
    _length_ = sd.random_number(10, 25)
    add_element_to_list(element=_x_, list_to_add=x_list)
    add_element_to_list(element=_y_, list_to_add=y_list)
    add_element_to_list(element=_length_, list_to_add=length_list)


while True:
    sd.clear_screen()
    stop = False
    for i, arg in enumerate(y_list):
        point = sd.get_point(x_list[i], y_list[i])
        sd.snowflake(center=point, length=length_list[i])
        y_list[i] -= 10
        x_list[i] -= sd.random_number(-10, 10)
        if y_list[i] < 20:
           stop = True
    sd.sleep(0.1)
    if stop:
        break
    if sd.user_want_exit():
        break


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


