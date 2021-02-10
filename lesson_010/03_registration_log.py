# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.
import os


class NotNameError(Exception):
    def __str__(self):
        return 'Поле name содержит НЕ только буквы'


class NotEmailError(Exception):
    def __str__(self):
        return 'Поле email НЕ содержит "@" и "."'


def read_line(line):
    try:
        name, email, age = line.split(' ')
    except ValueError:
        raise ValueError('НЕ присутсвуют все три поля')

    if not name.isalpha():
        raise NotNameError

    item_included = True
    for item in ['@', '.']:
        item_included *= item in email      # TODO: &= будет несколько точнее, чем *=
    if not item_included:
        raise NotEmailError

    # Я понимаю, что сначала первое условие прверяется, а затем уже второе.
    # Если наоборот, то код не сработает и вернет исключение для int(age) ValueError.
    # Правда в исходном списке нет такой ситуации, но проверить число ли введено было бы не плохо.
    if not (age.isdigit() and (10 <= int(age) <= 99)):
        raise ValueError('Поле age НЕ является числом от 10 до 99')


log_good = 'registrations_good.log'
log_bad = 'registrations_bad.log'

if os.path.isfile(log_good):
    os.remove(log_good)
if os.path.isfile(log_bad):
    os.remove(log_bad)

# TODO: указали кодировку 👍
with open('registrations.txt', 'r', encoding='utf8') as file:
    for line in file:
        # TODO: здесь лучше вызвать .strip() вместо [:-1]
        line = line[:-1]
        try:
            read_line(line=line)
        except (ValueError, NotNameError, NotEmailError) as exc:
            # TODO: а здесь не указали 😡
            with open(log_bad, 'a') as log_file:
                log_file.write(f'В строке "{line:^35}". Ошибка: {exc}.\n')
        else:
            # TODO: и здесь не указали 😡
            with open(log_good, 'a') as log_file:
                log_file.write(f'{line}\n')
print(f'Скрипт сработал. Log файлы записаны.')

# TODO и как итог на win10 машине:
#  
#  Traceback (most recent call last):
#   File "D:/job/skillbox/students_works/sobianin_nikolai/lesson_010/03_registration_log.py", line 72, in <module>
#     read_line(line=line)
#   File "D:/job/skillbox/students_works/sobianin_nikolai/lesson_010/03_registration_log.py", line 56, in read_line
#     raise ValueError('Поле age НЕ является числом от 10 до 99')
# ValueError: Поле age НЕ является числом от 10 до 99
#
# During handling of the above exception, another exception occurred:
#
# Traceback (most recent call last):
#   File "D:/job/skillbox/students_works/sobianin_nikolai/lesson_010/03_registration_log.py", line 75, in <module>
#     log_file.write(f'В строке "{line:^35}". Ошибка: {exc}.\n')
#   File "C:\Program Files\Python\Python38\lib\encodings\cp1252.py", line 19, in encode
#     return codecs.charmap_encode(input,self.errors,encoding_table)[0]
# UnicodeEncodeError: 'charmap' codec can't encode character '\u0412' in position 0: character maps to <undefined>
#
# Process finished with exit code 1