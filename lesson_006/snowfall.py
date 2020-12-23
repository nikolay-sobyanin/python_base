# -*- coding: utf-8 -*-

import simple_draw as sd

list_snowflakes = []


def get_snowflake():
    return {
        'x': sd.random_number(100, 1100),
        'y': sd.random_number(400, 600),
        'length': sd.random_number(10, 25),
    }


# ✅ создать_снежинки(N) - создает N снежинок
def create_snowflakes(N=40):
    global list_snowflakes
    for _ in range(0, N):
        list_snowflakes.append(get_snowflake())


# ✅ нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
def draw_snowflakes(color):
    for snowflake in list_snowflakes:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(center=point, length=snowflake['length'], color=color)


# ✅ сдвинуть_снежинки() - сдвигает снежинки на один шаг
def shifting_snowflakes():
    for snowflake in list_snowflakes:
        snowflake['y'] -= 10
        snowflake['x'] -= sd.random_number(-10, 10)


# ✅ номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
def numbers_reached_bottom_screen():
    list_numbers = []
    for i, snowflake in enumerate(list_snowflakes):
        if snowflake['y'] < 20:
            list_numbers.append(i)
    return list_numbers


# ✅ удалить_снежинки(номера) - удаляет снежинки с номерами из списка
def del_snowflakes(*numbers):   # TODO: единственное, что здесь не обязательно распковку использовать.
                                #  можно было и просто список передать.
    for i in sorted(numbers, reverse=True):
        list_snowflakes.pop(i)


#  Прочувствуйте название каждой функции, которая указана в описании задачи:
#  создать_снежинки(N) - создает N снежинок. Только создает. Не красит и не удаляет и не перемещает.
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color. Только красит и ничего больше.
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг. Только перемещает. Не красит, не создает и не удаляет.
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана.
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка. Не создает, не детектирует упашвшие.
#  .
#  Представьте это как врачей в больнице. Приходите к пульманологу (по легким), и просите его гипс наложить.
#  Пульманолог говорит: "вам в травмпункт!". Или врач-хирург, он конечно тоже врач и тоже работает с пациентами,
#  но его задача делать операции. В этом он хорош. А какой-нибудь терапевт или гинеколог - хороши в своем деле.
#  И таким образом, каждый занимается ТОЛЬКО своей нишей, для всех других создаются отдельные вакансии.
#  Организации, где врач играет сразу все роли (где-нибудь в Индии, в Бангладеше) работают существенно хуже.
#  В софте этот прицип применяется для того, чтобы можно было легко заменить 1 метод/функция/класс на другой.
#  Это можно представить как детское лего, если деталька будет слишком сложной формы, то ее придется собирать из
#  других деталей и скорее всего получится деталька-Франкентштейн. Слишком сложная форма - это ф-ция которая делает
#  несколько вещей сразу.
#  .
#  Вообще есть хороший способ проверить качественно ли написан код: если код легко модифицировать и проапргрейдить
#  значит код хорош) В коде, где ф-ция не сильно переплетены между собой, можно править 1 ф-цию не задевая все остальные
#  это существенно повышает скорость работы)
#  .
#  Вообще принципов больше, аббревиатура: S.O.L.I.D.
#  S - single responsibility (единство ответственности)
#  O - open|close (принцип открытости/закрытости)
#  L - Принцип Барбары Лисков
#  I - Принцип разделения интерфейсов
#  D - Принцип инверсий зависимостей
#  .
#  Мы пока познакомились с первым)
