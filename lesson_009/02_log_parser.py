# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
from collections import defaultdict


class LogParser:

    def __init__(self, file_name_in, file_name_out):
        self.file_name_in = file_name_in
        self.file_name_out = file_name_out
        self.list_log = []
        self.list_result = defaultdict(int)

    def parser(self):
        self.read_file()
        self.group_events()
        self.write_result_file()

    def read_file(self):
        with open(file=self.file_name_in, mode='r', encoding='utf8') as file:
            for line in file:
                # TODO: создать отдельный метод, который возвращает то, что нужно для данного вида сортировки:
                #  тип события и временную_метку. Для разных подклассов будет совершенно разный способ парсинга
                #  строки. Прям может быть вообще разный! Профит: разные файлый, разный формат, но алгоритм одинаков,
                #  и хранится в главном файле. Отличие между классами будет только в "parse_line".
                date = line[1:11]
                time = line[12:17]
                status = line[29:-1]
                year = date[0:4]
                month = date[5:7]
                day = date[8:10]
                hour = time[0:2]
                minute = time[3:5]
                self.list_log.append({
                    'year': year,
                    'month': month,
                    'day': day,
                    'hour': hour,
                    'minute': minute,
                    'status': status,
                })

    def group_events(self):
        for log in self.list_log:
            time_log = f'[{log["year"]}-{log["month"]}-{log["day"]} {log["hour"]}:{log["minute"]}]'
            if log['status'] == 'NOK':
                self.list_result[time_log] += 1

    def write_result_file(self):
        with open(file=self.file_name_out, mode='w', encoding='utf8') as file:
            for time, res in self.list_result.items():
                line = f'{time} {res}\n'
                file.write(line)


file_name_in = 'events.txt'
file_name_out = 'out.txt'
LogParser(file_name_in=file_name_in, file_name_out=file_name_out).parser()




# После зачета первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
