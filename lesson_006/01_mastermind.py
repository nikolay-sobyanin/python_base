# -*- coding: utf-8 -*-

# Игра «Быки и коровы»
# https://goo.gl/Go2mb9
#
# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число c неповторяющимися цифрами,
# компьютер сообщают о количестве «быков» и «коров» в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1


# Составить отдельный модуль mastermind_engine, реализующий функциональность игры.
# В mastermind_engine нужно реализовать функции:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной.
# Обратите внимание, что строки - это список символов.
#
# В текущем модуле (lesson_006/01_mastermind.py) реализовать логику работы с пользователем:
#   модуль движка загадывает число
#   в цикле, пока число не отгадано
#       у пользователя запрашивается вариант числа
#       проверяем что пользователь ввел допустимое число (4 цифры, все цифры разные, не начинается с 0)
#       модуль движка проверяет число и выдает быков/коров
#       результат быков/коров выводится на консоль
#  когда игрок угадал таки число - показать количество ходов и вопрос "Хотите еще партию?"
#
# При написании кода учитывайте, что движок игры никак не должен взаимодействовать с пользователем.
# Все общение с пользователем (вывод на консоль и запрос ввода от пользователя) делать в 01_mastermind.py.
# Движок игры реализует только саму функциональность игры. Разделяем: mastermind_engine работает
# только с загаданным числом, а 01_mastermind - с пользователем и просто передает числа на проверку движку.
# Это пример применения SOLID принципа (см https://goo.gl/GFMoaI) в архитектуре программ.
# Точнее, в этом случае важен принцип единственной ответственности - https://goo.gl/rYb3hT

from mastermind_engine import get_number, print_number, check_number

new_game = True

while True:
    if new_game:
        print('----Новая игра----')
        get_number()
        print(print_number())
        n = 0
        new_game = False

    enter_number = input('Введите число: ')
    if not enter_number.isdigit():
        print('Неккоректно введено число! Имеются недопустимые символы.')
        continue
    if len(enter_number) != 4:
        print('Неккоректно введено число! Длина числа должна быть равна 4 символам.')
        continue
    if int(enter_number[0]) == 0:
        print('Неккоректно введено число! Число не должно начинатся на 0.')
        continue
    number_repeat = False
    for i in range(0, len(enter_number) - 1):
        for j in range(i + 1, len(enter_number)):
            if enter_number[i] == enter_number[j]:
                number_repeat = True
    if number_repeat:
        print('Неккоректно введено число! Имеются повторяющиеся цифры в числе.')
        continue

    bulls = check_number(enter_number=enter_number)['bulls']
    cows = check_number(enter_number=enter_number)['cows']
    print(f'быки - {bulls}, коровы - {cows}')
    n += 1
    if bulls == 4:
        print(f'Игра окончена. Количество ходов - {n}')
        next_game = input('Хотите еще партию? ')

        if next_game.lower() in ['да', 'yes']:
            new_game = True
            print()
            print()
        else:
            break

print('Спасибо за игру!')

# зачет!