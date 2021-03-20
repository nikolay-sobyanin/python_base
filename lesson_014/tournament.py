from collections import defaultdict

from bowling import PlayerResult

# Работает, но мне не нравится как написан код, решил отправить что бы получить обратную связь и на выходных было чем
# заняться.
#
# Перое. Что за магия с разным размером табуляции в исходнои файле?! Гуглил очень много времени не нашел, как сделать.
# TODO: о каком из файлов именно идет речь?
# Вот это имею ввиду. В файле для обработки. Между именем и результатом пробелы разного размера,
# как я понял это табуляция
# Татьяна	62334/6/4/44X361/X
# Давид	--8/--8/4/8/-224----


# Второе. Структура кода в классе. Основаная проблема не понятно как возвращаться continue из функции, а также
# нужно локальные переменные как то передавать между функциями. Как то очень сложно получается. А в таком виде код не
# динамически не изменяемый.
# TODO: насколько понял вопрос: не нравится, что у нас в классе Парсера одна мега функция, которая все почти делает.
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

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
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
                        win_name, win_score = None, 0
                        output_file.write(line + '\n')
                        tour_start = True
                        continue
                    elif line.startswith('winner is'):
                        output_file.write(f'winner is {win_name}\n\n')
                        tour_start = False
                        continue

                    if tour_start:
                        name, game_result = line.split('\t')
                        player = PlayerResult(name, game_result)

                        try:
                            player.get_score()
                        except ValueError as exc:
                            print(f'Произошла ошибка в туре {numb_tour}. Строка: {name} {game_result}.\n'
                                  f'Ошибка: {exc}\n')
                            continue

                        if player > win_score:
                            win_name, win_score = player.name_player, player.score
                            self.win_games[name] += 1

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


tournament = TournamentBowling('tournament.txt', 'result_tournament.txt')
tournament.get_result_tournament()
tournament.print_result_tournament()

