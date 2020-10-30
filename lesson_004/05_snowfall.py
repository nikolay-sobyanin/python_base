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


# TODO: удобнее будет создать 1 список, который будет хранить N маленьких словарей.
#  Каждый словарик будет иметь 3 ключа: 'x', 'y', 'length'.
#  .
#  Например, чтобы обратиться к значению 'Y' у 10ой снежинке можно будет использовать:
#       snowflakes[9]['y'] -= 10
#  .
#  Преимущество в том, что мы можем обходить список в цикле, и обращаться к его элементам, как к объектам-снежинкам,
#  при этом удачно подобранные имена ключей 'x', 'y' сохраняют читабельность кода.
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

    # TODO: sd.user_want_exit()
    #  Это функция, которая возвращает True, если пользователь захотел выйти. До тех
    #  пор пока он не решил выйти, функция всегда возвращает False.
    #  .
    #  В while, вместо TRUE можно подставить вызов этой функции. И цикл будет длиться до тех пор, пока пользователь не
    #  решит выйти. Только учтите, должно читаться как:
    #   "ЦИКЛ пока пользователь НЕ хочет выйти"
    #  Сейчас читается как:
    #   "ЕСЛИ пользователь хочет выйти"
    #  .
    #  Логично, что вместо:
    #  .
    #  while True:
    #     if x > 100500:
    #         break
    #     print('ola!')
    #  Можно сделать:
    #  .
    #  while x <= 100500:
    #     print('ola!')
    if sd.user_want_exit():
        break

# TODO: Добавить start_drawing в начало итерации, а finish_drawing - в конец.
#  start_drawing() запрещает рисовать что-то, пока запрет не будет снят вызовом finish_drawing().
#  Куда деваются все изменения? Копятся в буфере.
#  Когда мы вызываем sd.finish_drawing() все накопишиеся изменения отображаются на экране.
#  .
#  Зачем так надо?
#  Дело в том, чтоб сама операция "нарисовать что-то на экране" - это медленная операция. Поэтому нам выгодно не
#  каждую черточку рисовать сразу, а сначала все изменения накопить, а только потом вывести их на экран 1 вызовом.
#  .
#  Аналогия: можно заполнить грузовик всеми вещами за 4 часа и перевести их, или же перевозить по 1 вещи.
#  Второй способ удобен, если нужно очень срочно, а первый оптимален, если можно немного подождать.
#  .
#  Первый способ - это наш) Надеюсь принцип работы sd.start_drawing() и sd.finish_drawing() теперь понятен. Он важен,
#  нужен и пригодится еще в 5 и 6 модулях.


# TODO: start_drawing вызывается в самом начале итерации цикла while. Она запрещает рисовать что-то, пока
#  запрет не будет снят вызовом finish_drawing. Куда деваются все изменения? Копятся в буфере.
#  Запрос к устройствам ввода и вывода всегда супер медленные, пока мы остаемся между ЦП и ОЗУ, у нас довольно
#  приемлемая скорость работы. Скорость работы устройств:
#         |--------------------------------------------------------------------|
#         |Устройство   |   Тактов ЦП   |   Пропорционал. "человеческая" шкала |
#         |--------------------------------------------------------------------|
#         |Кэш L1       |            3         3 секунды                       |
#         |Кэш L1       |           14         14 сек.                         |
#         |ОЗУ          |          250         250 сек.                        |
#         |диск         |   41 000 000         1.3 года                        |
#         |сеть         |  240 000 000         7.6 лет                         |
#         |--------------------------------------------------------------------|
#  .
#  Запрос к монитору - это можно сказать "около года" в "человеческой шкале". Поэтому мы вызываем start_drawing,
#  копим изменения в ОЗУ (тратим "человечески секунды"), а потом, когда время настало - вызываем finish_drawing.
#  .
#  Т.е. рисуем все, что накопилось в буфере на экране.

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


