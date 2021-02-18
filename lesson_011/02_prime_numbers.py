# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел
import math


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
    right_numb = numb[-(size_numb // 2):]
    left_sum = sum(map(int, left_numb))
    right_sum = sum(map(int, right_numb))
    return left_sum == right_sum


def palindromic_numb(numb):
    numb = str(numb)
    size_numb = len(numb)
    if size_numb == 1:
        return False
    return numb == numb[::-1]


def natural_numb(numb):
    if numb <= 0:
        return False
    if numb == int(numb):
        return True
    else:
        return False


def triangular_numb(numb):
    """Формула для определения треугольного числа numb = n * (n + 1) / 2. Если квадратное уравнение имеет хотя бы один
    корень равный натуральному числу, то число треугольное."""
    if numb <= 0:
        return False
    # n^2 + n + (-2 * numb) = 0
    a, b, c = 1, 1, -2 * numb
    D = b ** 2 - 4 * a * c
    if D < 0:
        return False
    if D == 0:
        x = -b / (2 * a)
        return natural_numb(x)
    if D > 0:
        x1 = (-b - math.sqrt(D)) / (2 * a)
        x2 = (-b + math.sqrt(D)) / (2 * a)
        if natural_numb(x1) or natural_numb(x2):
            return True
        return False


# lucky_and_prime_numbers = filter(lucky_numb, prime_numbers_generator(n=10000))
lucky_and_prime_numbers = [x for x in prime_numbers_generator(n=10000) if lucky_numb(x)]

# palindromic_and_prime_numbers = filter(palindromic_numb, prime_numbers_generator(n=10000))
palindromic_and_prime_numbers = [x for x in prime_numbers_generator(n=10000) if palindromic_numb(x)]

# triangular_and_prime_numbers = filter(triangular_numb, prime_numbers_generator(n=10000))
triangular_and_prime_numbers = [x for x in prime_numbers_generator(n=10000) if triangular_numb(x)]

for number in triangular_and_prime_numbers:
    print(number)


