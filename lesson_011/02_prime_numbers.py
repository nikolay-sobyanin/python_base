# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers

# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        self.i = 1
        self.prime_numbers = []
        return self

    def __next__(self):
        while self.i < self.n:
            self.i += 1
            for prime in self.prime_numbers:
                if self.i % prime == 0:
                    break
            else:
                self.prime_numbers.append(self.i)
                return self.i
        raise StopIteration


# print(f'{"Итератор":-^20}')
# prime_number_iterator = PrimeNumbers(n=100)
# for number in prime_number_iterator:
#     print(number)


# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            yield number


# print(f'{"Генератор":-^20}')
# for number in prime_numbers_generator(n=100):
#     print(number)


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
# TODO: если что - должно быть 3 функции. См.описание части 3.
#  (не хватает 2х функций).

def lucky_numb(numb):
    numb = str(numb)
    size_numb = len(numb)
    if size_numb == 1:
        return False
    left_numb = numb[:size_numb // 2]

    # TODO: используйте срез с отрицательным индексом, чтобы 4 строки ниже превратить в 1
    if size_numb % 2 == 0:
        right_numb = numb[size_numb // 2:]
    else:
        right_numb = numb[size_numb // 2 + 1:]
    left_sum = sum(map(int, left_numb))
    right_sum = sum(map(int, right_numb))
    return left_sum == right_sum


# TODO: применено верно
lucky_and_prime_numbers = filter(lucky_numb, prime_numbers_generator(n=10000))
for number in lucky_and_prime_numbers:
    print(number)


