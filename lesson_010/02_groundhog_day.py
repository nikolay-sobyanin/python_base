# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.
from random import randint, choice
import os


class IamGodError(Exception):
    pass


class DrunkError(Exception):
    pass


class CarCrashError(Exception):
    pass


class GluttonyError(Exception):
    pass


class DepressionError(Exception):
    pass


class SuicideError(Exception):
    pass


list_exception = [
        IamGodError('Я бог!'),
        DrunkError('Я пил!'),
        CarCrashError('Я попал в аварию!'),
        GluttonyError('Я переел!'),
        DepressionError('Я в депрессии!'),
        SuicideError('Я думал о суициде!')
    ]


def one_day():
    if randint(1, 13) == 1:
        raise choice(list_exception)
    return randint(1, 7)


ENLIGHTENMENT_CARMA_LEVEL = 777
carma_level = 0
day = 0

log_file_name = 'log_error.txt'
if os.path.isfile(log_file_name):
    os.remove(log_file_name)

while carma_level < ENLIGHTENMENT_CARMA_LEVEL:
    day += 1
    try:
        carma_level += one_day()
    except (IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError) as exc:
        carma_level -= 20
        with open(log_file_name, 'a') as log_file:
            log_file.write(f'День № {day:0>3}. Уровень кармы {carma_level:0>3}. {exc}\n')
print(f'Скрипт сработал. Всего прожито дней {day}. Записан файл ошибок {log_file_name}')

# https://goo.gl/JnsDqu
