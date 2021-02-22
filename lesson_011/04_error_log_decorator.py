# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'
import os


def log_errors(name_log):
    def log(func):
        if os.path.isfile(name_log):
            os.remove(name_log)

        def surrogate(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                name_func = func.__name__
                with open(name_log, 'a', encoding='utf8') as log_file:
                    log_file.write(f'{name_func:^15} {str(args):^35} {str(kwargs):^30} {str(type(exc)):^30}: {exc}.\n')
                raise
        return surrogate
    return log


# Проверить работу на следующих функциях
@log_errors('function_errors.log')
def perky(param):
    return param / 0


@log_errors('function_errors.log')
def check_line(line):
    name, email, age = line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]


for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')

perky(param=42)

# зачет!