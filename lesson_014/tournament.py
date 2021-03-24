from collections import defaultdict

from bowling import PlayerResult, Global, Local

# Работает, но мне не нравится как написан код, решил отправить что бы получить обратную связь и на выходных было чем
# заняться.
#
# Перое. Что за магия с разным размером табуляции в исходнои файле?! Гуглил очень много времени не нашел, как сделать.
# о каком из файлов именно идет речь?
# Вот это имею ввиду. В файле для обработки. Между именем и результатом пробелы разного размера,
# как я понял это табуляция
# Татьяна	62334/6/4/44X361/X
# Давид	--8/--8/4/8/-224----

#  да, верно. Табуляция.
#  Первый. Какой у табов символ? Например "перевод каретки (курсора) на новую строку" это "\n". А у таба что?
#  .
#  Второе. Насколько помню, '1  2	3'.split() по умолчанию сработает на табы и пробелы.

#  Это все понятно. Знак табуляции \t. Вопрос в том, что табуляция в файле имеет различный размер. Где то она равна
# 2-ум пробелам, где то трем и тд. За счет этого достигается выравнивание текса в исходном файле. Мне интересно как
# сделали этот разный размер табуляции?

#  таб - это не просто 3-4 пробела.
#  Никогда не пробовал объяснить как работает табуляция. Попробую конечно, но лучше с нею еще в notepad++ поиграться.
#  Примечание: будем считать, что 1 таб == 4 пробела.
#  .
#  Итак:
#  Когда мы ставим 8 пробелов - это 8 пробелов.
#  Когда только 2 таба - это расстояние эквивалентное 8 пробелам.
#  НО если мы ПЕРЕД табом поставим 2 пробела, то ТАБ, как-бы сожмется до 2х пробелов.
#  Если повтрим фокус с 3 пробелами, то визуально ТАБ станет сожмется до 1го пробела.
#  НО если попробуем поставить 4 пробела, то ТАБ как-бы отпружинит, и у нас станет 4 отдельных проблеа и 1 таб.
#  .
#  ИТОГО: таб может сжиматься, пока замещающие его пробелы, не вытеснят его полностю.


# Второе. Структура кода в классе. Основаная проблема не понятно как возвращаться continue из функции, а также
# нужно локальные переменные как то передавать между функциями. Как то очень сложно получается. А в таком виде код не
# динамически не изменяемый.
# насколько понял вопрос: не нравится, что у нас в классе Парсера одна мега функция, которая все почти делает.
#  Можно сделать более ОППэшно, но всё всегда зависит от времени и ТЗ:
#   * если нам говорят: "пиши толково, парсер будет расширяться и дополняться", то мы будет делать так:
#          вводим классы:
#           Игрок - кто, что и почем;
#           Турнин - набор из игроков + немного инфы о турнире
#           ПарсерТурниров - читает блокнот и собирает турниры
#           БизнесЛогика - определяет кто победил и пишит результат
#   * если нам говорят: забей, надо быстро, это на 1 неделю, дальше добавлять ничего не планируем - пишим 1 класс
#     как этот, и не паримся с разбиением и кучей файлов.


# Третье. Создал два defaultdict(int), я понимаю что можно defaultdict(dict), но не получилось записывать в них.
# Или как то по другому делается счетсчик на два параметра?
#  или можно один defaultdict(int).
#  А вообще можно собстенную функция скормить:
#   >>> d = defaultdict(lambda: [1,2,3])
#   >>> d[1]
#   [1, 2, 3]
#   >>> d
#   defaultdict(<function <lambda> at 0x0000026DF1A6D160>, {1: [1, 2, 3]})


class TournamentBowling:

    def __init__(self, input_file, output_file, rules='local'):
        self.input_file = input_file
        self.output_file = output_file
        self.rules = rules
        self.win_games = defaultdict(int)

    def get_result_tournament(self):
        with open(self.input_file, 'r', encoding='utf8') as input_file:
            with open(self.output_file, 'w', encoding='utf8') as output_file:
                for line in input_file:
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith('### Tour'):
                        *_, numb_tour = line.split()
                        win_player = None
                        output_file.write(line + '\n')
                        tour_start = True
                        continue
                    elif line.startswith('winner is'):
                        output_file.write(f'winner is {win_player.name_player}\n\n')
                        self.win_games[win_player.name_player] += 1
                        tour_start = False
                        continue

                    if tour_start:
                        name, game_result = line.split('\t')
                        if self.rules.upper() == 'GLOBAL':
                            player = PlayerResult(name, game_result, Global())
                        elif self.rules.upper() == 'LOCAL':
                            player = PlayerResult(name, game_result, Local())
                        else:
                            raise ValueError(f'Неверно введен параметр "rules" {self.rules}.')

                        try:
                            player.compute_score()
                        except ValueError as exc:
                            print(f'Произошла ошибка в туре {numb_tour}. '
                                  f'Строка: {player.name_player} {player.game_result}.\n'
                                  f'Ошибка: {exc}\n')
                            continue

                        if win_player is None or player > win_player:
                            win_player = player

                        output_file.write(player.__str__() + '\n')

    def print_result_tournament(self):
        column_width = 10
        line = 2 * f'+{"":-^{column_width}}' + '+'
        print(line)
        print(f'|{"Участник":^{column_width}}|{"Побед":^{column_width}}|')
        print(line)
        for name, win_games in self.win_games.items():
            print(f'|{name:^{column_width}}|{win_games:^{column_width}}|')
            print(line)


def main():
    tournament_local = TournamentBowling('tournament.txt', 'result_local_tournament_01.txt', rules='local')
    tournament_local.get_result_tournament()
    tournament_local.print_result_tournament()

    tournament_external = TournamentBowling('tournament.txt', 'result_external_tournament_01.txt', rules='global')
    tournament_external.get_result_tournament()
    tournament_external.print_result_tournament()


if __name__ == '__main__':
    main()
