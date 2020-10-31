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


sd.resolution = (1200, 600)
N = 40
list_snowflakes = []

for i in range(0, N):
    # TODO: "_x_", "_y_" - нетипичные имена. Идея в том, чтобы показать, что это приватные переменные? тогда достаточно "_х".
    #  Челлендж! Ужать все строки ниже в одну. И да, можно напрямую list_snowflakes.append({...}).
    #  add_element_to_list вызывается только в одном месте, и его наличие не оправдано.
    _x_ = sd.random_number(100, 1100)
    _y_ = sd.random_number(400, 600)
    _length_ = sd.random_number(10, 25)
    _add_to_list_ = {
        'x': _x_,
        'y': _y_,
        'length': _length_,
    }
    add_element_to_list(element=_add_to_list_, list_to_add=list_snowflakes)

while not sd.user_want_exit():
    sd.start_drawing()
    # sd.clear_screen()
    stop_draw = False
    for snowflakes in list_snowflakes:
        point = sd.get_point(snowflakes['x'], snowflakes['y'])
        sd.snowflake(center=point, length=snowflakes['length'], color=sd.background_color)

        snowflakes['y'] -= 10
        snowflakes['x'] -= sd.random_number(-10, 10)

        new_point = sd.get_point(snowflakes['x'], snowflakes['y'])
        sd.snowflake(center=new_point, length=snowflakes['length'], color=sd.COLOR_WHITE)

        # TODO: если снежинка упала - добавляем в список новую снежинку, а это убираем из него.
        #  Т.о. у нас образуется сугроб.
        if snowflakes['y'] < 20:
            stop_draw = True

    # TODO: можно убрать
    if stop_draw:
        break
    sd.finish_drawing()
    sd.sleep(0.1)


# TODO: сейчас у нас алгоритм работает целенаправленно по одной снежинке: взяли одну, стрели, сдвинули, нарисовали.
#  Пока мы работаем в таком режиме, у нас при пересечении снежинок происходит перетирание их друг другом.
#  Т.е. взяли одну, стерли ее + кусочки тех с кем пересеклась, сдвинули, нарисовали. А кусочки, которые стерли
#  не перерисовали. Когда возьмем следующую снежинки - история повторится. В итоге, в каждый момент времени у нас
#  на пересечении снежинок возникает рябь. Какие светлые мысли будут, как это одолеть?

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
