# -*- coding: utf-8 -*-

from random import randint

_generated_number = {}
_sorted_keys = []


def get_number():
    global _generated_number, _sorted_keys

    for i in range(1, 5):
        if i == 1:
            _generated_number[i] = randint(1, 9)
            continue
        new_number = 0
        number_repeat = True
        while number_repeat:
            new_number = randint(0, 9)
            number_repeat = False
            for j in _generated_number:
                if _generated_number[j] == new_number:
                    number_repeat = True
        _generated_number[i] = new_number
    _sorted_keys = sorted(_generated_number.keys())


def print_number():
    number = ''

    for key in _sorted_keys:
        number += str(_generated_number[key])
    print(number)


def check_number(enter_number):
    dict_enter_number = {}
    bulls_and_cows = {'bulls': 0, 'cows': 0}

    for i, number in enumerate(enter_number):
        dict_enter_number[_sorted_keys[i]] = int(number)

    for i in _sorted_keys:
        if dict_enter_number[i] == _generated_number[i]:
            bulls_and_cows['bulls'] += 1
        for j in _generated_number:
            if dict_enter_number[i] == _generated_number[j]:
                bulls_and_cows['cows'] += 1
    if bulls_and_cows['bulls'] != 0:
        bulls_and_cows['cows'] -= bulls_and_cows['bulls']

    return bulls_and_cows
