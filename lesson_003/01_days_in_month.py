# -*- coding: utf-8 -*-

# (if/elif/else)

# По номеру месяца вывести кол-во дней в нем (без указания названия месяца, в феврале 28 дней)
# Результат проверки вывести на консоль
# Если номер месяца некорректен - сообщить об этом

# Номер месяца получать от пользователя следующим образом
user_input = input('Введите, пожалуйста, номер месяца: ')
month = int(user_input)
print('Вы ввели', month)

# TODO: работает верно, но чтобы мы делали, если бы писали код для календаря с Юпиретра, где 1 год длится 12 земных лет,
#  т.е. 144 месяца по 30 дней! Неужели мы бы написали 144 условия? Конечно нет, мы бы придумали другой способ.
#  .
#  Лучший способ решения этой задачи - это использование списка/кортежа для хранения кол-ва дней в каждом месяце.
#  В нем может храниться информация о том, сколько дней в каждом месяце. Всего будет 12 элементов, т.е. 12 месяцев.
#  Пользователь вводит число 1 - значит программа выдает ему 1ый элемент списка, пользователь вводит 12 - получает
#  последний элемент.
#  .
#  Формат вывода лучше тогда сделать:
#       "В X месяце Y дн.".

if month == 1:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 2:
    quantity_day = 28
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 3:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 4:
    quantity_day = 30
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 5:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 6:
    quantity_day = 30
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 7:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 8:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 9:
    quantity_day = 30
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 10:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 11:
    quantity_day = 30
    print(f'Количество дней в месяце №{month}: {quantity_day}')
elif month == 12:
    quantity_day = 31
    print(f'Количество дней в месяце №{month}: {quantity_day}')
else:
    print('Неверно указан номер месяца')