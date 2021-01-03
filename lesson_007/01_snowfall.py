# -*- coding: utf-8 -*-

import simple_draw as sd


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:

    def __init__(self):
        self.x = sd.random_number(100, 1100)
        self.y = sd.random_number(400, 600)
        self.length = sd.random_number(10, 25)

    def clear_previous_picture(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.background_color)

    def move(self):
        self.y -= 10
        self.x -= sd.random_number(-10, 10)

    def draw(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.COLOR_WHITE)

    def can_fall(self):
        # TODO: избавьтесь от if/else. Пример:
        #  def is_even(x):
        #     return x % 2 == 0
        if self.y < 20:
            return False
        else:
            return True


list_flakes = []


def get_flakes(count=40):
    for _ in range(0, count):
        list_flakes.append(Snowflake())
    return list_flakes


# TODO: функция "вернуть упавшие снежинки", а сама удаляет их из списока.
#  Если pop выполняется внутри цикла по списку, из которого pop`аем, то часть элементов будет пропущена.
#  Т.е. текущий вариант еще и не точно срабатывает. Разделите на 2 функции, на подобии 02 задачи 06 модуля.
def get_fallen_flakes():
    count = 0
    for i, snowflake in enumerate(list_flakes):
        if not snowflake.can_fall():
            list_flakes.pop(i)
            count += 1
    return count


def append_flakes(count):
    # TODO: range(0, count) == range(count)
    for _ in range(0, count):
        list_flakes.append(Snowflake())


sd.resolution = (1200, 600)

# flake = Snowflake()

# while not sd.user_want_exit():
#     sd.start_drawing()
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.finish_drawing()
#     sd.sleep(0.1)


# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:

N = 40

flakes = get_flakes(count=N)  # создать список снежинок

while not sd.user_want_exit():
    sd.start_drawing()
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
    if fallen_flakes:
        append_flakes(count=fallen_flakes)  # добавить еще сверху
    sd.finish_drawing()
    sd.sleep(0.1)

sd.pause()
