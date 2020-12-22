# -*- coding: utf-8 -*-

from random import sample
from operator import itemgetter

_generated_number = []
NUMB_OF_DIGITS = 4
NUMBERS = '0123456789'


#   загадать_число()
def get_number():
    global _generated_number
    _generated_number = sample(NUMBERS, NUMB_OF_DIGITS)
    if _generated_number[0] == '0':
        _generated_number.append(sample(set(NUMBERS) - set(_generated_number), 1)[0])
        _generated_number.pop(0)


#   распечатать_число()
def print_number():
    number_print = ''
    for number in _generated_number:
        number_print += number
    return number_print


#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
def check_number(enter_number):
    dict_enter_number = {}
    bulls_and_cows = {'bulls': 0, 'cows': 0}

    for i, number in enumerate(enter_number):
        dict_enter_number[number] = i    # ключ - цифра, значение - позиция цифры. Далее сортировка по значениям.

    for element in sorted(dict_enter_number.items(), key=itemgetter(1)):
        if element[0] == _generated_number[element[1]]:
            bulls_and_cows['bulls'] += 1
        elif element[0] in _generated_number:
            bulls_and_cows['cows'] += 1

    return bulls_and_cows

    #  Только с поправкой на то, что вы написали, что это специально для закрепления знаний, мы оставим.
    #  Но превращать список в словарь не стоит.
    #  А хранить отсортированные ключи словаря - это вообще нонсанс.
    #  .
    #  Как тогда получить отсортированные данные из словаря?
    #  Использовать параметр 'key' у функции sorted.
    #  Пусть есть словарь d, скормим его .items() функции sorted() и посмотрим что вышло:
    #       d = {'b': 1, 'a': 2, 'c':3}
    #       print(sorted(d.items()))            # [('a', 2), ('b', 1), ('c', 3)]
    #  .
    #  Ф-ция сортировки отсортировала список пар. Каждая пара ключ-значения представлена в виде кортежа.
    #  .
    #  Когда мы добавляем 'key', мы указываем, что сортировать нужно по какому-то критерию, который должен
    #  высчитываться для каждого элемента списка, т.е. для каждой пары.
    #  Пример:
    #       # импортируем функцию, которая принимает индекс и выдает значение по нему, можно сказать
    #       # что itemgetter - это и есть квадратные скобки '[]'
    #       from operator import itemgetter
    #       .
    #       # .items() возвращает пары ключ-значение в виде кортежей. Поэтому здесь происходит сортировка
    #       # списка пар ключ-значение. При этом в качестве ключа (критерия) кортировки берется значение,
    #       # которое возвращает itemgetter для 1го (не 0го, а 1го) элемента. Т.е. для значения списка.
    #       sorted(d.items(), key=itemgetter(1))
    #  .
    #  itemgetter(1) берет каждую пару и возвращает последний элемент: 2, 1, 3. Получив критерии по которым
    #  нужно сортировать элементы, функция sort выполняет сортировку:
    #        print(sorted(d.items(), key=itemgetter(1)))           # [('b', 1), ('a', 2), ('c', 3)]
    #  .
    #  В итоге, мы получаем список из котрежей, где 0ое значение - значения словаря, а 1ое значение - ключ
    #  словаря. При этом, этот набор отсортирован по значениям! То, что нужно)
    #  .
    #  Сортировать словарь - непростая задача. Совсем. Есть более удобный способ, но он еще более сложный,
    #  использует словарные включения. Поэтому мы пока остановимся на этом способе.

