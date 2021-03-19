from collections import defaultdict

from bowling import PlayerResult

# Работает, но мне не нравится как написан код, решил отправить что бы получить обратную связь и на выходных было чем
# заняться.
#
# Перое. Что за магия с разным размером табуляции в исходнои файле?! Гуглил очень много времени не нашел, как сделать.
#
# Второе. Структура кода в классе. Основаная проблема не понятно как возвращаться continue из функции, а также
# нужно локальные переменные как то передавать между функциями. Как то очень сложно получается. А в таком виде код не
# динамически не изменяемый.
#
# Третье. Создал два defaultdict(int), я понимаю что можно defaultdict(dict), но не получилось записывать в них.
# Или как то по другому делается счетсчик на два параметра?
#
# Четвертое. Создавать логгер для записи ошибок при расчете результата? Пока что ошибки пишу в консоль.


class TournamentBowling:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.quantity_games = defaultdict(int)
        self.win_games = defaultdict(int)

    def get_result_tournament(self):
        with open(self.input_file, 'r', encoding='utf8') as input_file:
            with open(self.output_file, 'w', encoding='utf8') as output_file:
                for line in input_file:
                    line = line.strip()

                    if line.startswith('### Tour'):
                        _, _, numb_tour = line.split(' ')
                        winner_tour = {'name': None, 'score': 0}
                        output_file.write(line + '\n')
                        tour_start = True
                        continue
                    elif line.startswith('winner is'):
                        output_file.write(f'winner is {winner_tour["name"]}\n\n')
                        tour_start = False
                        continue

                    if tour_start:
                        name, game_result = line.split('\t')
                        player = PlayerResult(name, game_result)
                        try:
                            player.get_score()
                        except ValueError as exc:
                            print(f'Произошла ошибка в туре {numb_tour}. Строка: {name} {game_result}.\n'
                                  f'Ошибка: {exc}\n')  # Пока что пишу в консоль. По хорошему нужно в лог ошибок писать
                            continue
                        output_file.write(f'{name:<8}{game_result:<24}{player.score}\n')
                        self.quantity_games[name] += 1

                        if int(player.score) > winner_tour['score']:
                            winner_tour['name'] = name
                            winner_tour['score'] = player.score
                            self.win_games[name] += 1

    def print_result_tournament(self):
        for name, quantity_games in self.quantity_games.items():
            print(f'|{name:<8}|{quantity_games:^10}|{self.win_games[name]:^10}|')


tournament = TournamentBowling('tournament.txt', 'result_tournament.txt')
tournament.get_result_tournament()
tournament.print_result_tournament()

