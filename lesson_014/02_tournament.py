# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна


# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>
import argparse

from tournament_01 import TournamentBowling
from bowling import Local, Global


def main():
    parser = argparse.ArgumentParser(description="Get tournament's score. --input_file --output_file")
    parser.add_argument('--input_file', required=True, type=str, help='Input file')
    parser.add_argument('--output_file', required=True, type=str, help='Output file')
    parser.add_argument('--rules', required=True, type=str, help='Local or World')
    args = parser.parse_args()

    if args.rules.upper() == 'WORLD':
        rules = Global()
    else:
        rules = Local()

    tournament = TournamentBowling(input_file=args.input_file, output_file=args.output_file, rules=rules)
    tournament.get_result_tournament()
    tournament.print_result_tournament()


if __name__ == '__main__':
    main()

# python 02_tournament.py --input_file tournament.txt --output_file result.txt --rules World

# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+

# зачет!