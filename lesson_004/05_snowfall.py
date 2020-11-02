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

# TODO: если переменная ("i") не используется, но необходима. Как в for цикле, ее принято заменять на "_".
#  "_" - это переменная, значение которой не важно, не используется. Т.е. эта такая же переменная как и все остальные
#  но название стилистически подобрали так, что она "пустое место". Пример:
#   for _ in range(3):
#       print('ну купи слона!')
for i in range(0, N):
    list_snowflakes.append({
        'x': sd.random_number(100, 1100),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    })

while not sd.user_want_exit():
    sd.start_drawing()
    # sd.clear_screen()
    # TODO: enumerate можно убрать.
    #  "for cur_snowflake in snowflakes:"       -  рабочий вариант
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
            # TODO: вот тут дублируется код "вернуть снежинку".
            #  Как круто мы можем сделать:
            #   1. создаем функцию "вернуть снежинку". Эта функция возвращает словарь-снежинку;
            #   2. вызываем эту функцию в двух местах:
            #       2.1. выше, где добавляли снежинки;
            #       2.2. здесь, где вместо того, чтобы удалять снежинку из списка, мы воспользуемся метод update() у
            #            словаря-снежинки.
            #   .
            #   Профит:
            #   1. если правила создания снежинки изменятся - придется править только в одном месте - функцию "вернуть
            #      снежинку";
            #   2. мы не будет добавлять/удалять элементы списка, что позволит нам выиграть 2 вещи сразу:
            #       2.1. удаление из списка вызывает операцию пересоздания словаря. Не самый быстрый процесс;
            #       2.2. если мы удаляем из списка, находясь в цикле по списку, мы пропускаем идущий следом элемент.
            #            Т.е. pop(0) вызов пропуск элемента 1. Т.к. все элементы сдвинутся, и первый станет 0ым.
            #            А нулевой мы уже обслужили и перейдем к 1ому.
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
