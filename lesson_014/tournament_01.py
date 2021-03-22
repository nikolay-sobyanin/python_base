from collections import defaultdict

from bowling import PlayerResult


class TournamentBowling:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.parser_tour = ParserTour(self.input_file)
        self.win_games = defaultdict(int)

    def get_result_tournament(self):
        with open(self.output_file, 'w', encoding='utf8') as output_file:
            for line in self.parser_tour.read_file():

                if self.parser_tour.start_tour(line):
                    numb_tour = self.parser_tour.get_numb_tour(line)
                    tour = Tour(numb_tour)
                    output_file.write(line + '\n')
                    continue
                elif self.parser_tour.end_tour(line):
                    self.win_games[tour.win_player.name_player] += 1
                    output_file.write(f'winner is {tour.win_player.name_player}\n\n')
                    tour = None

                if tour is not None:
                    name, game_result = self.parser_tour.get_name_result(line)
                    try:
                        player = tour.get_result_player(name, game_result)
                    except ValueError:
                        continue

                    tour.get_win_player(player)
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


class ParserTour:

    def __init__(self, input_file):
        self.input_file = input_file

    def read_file(self):
        with open(self.input_file, 'r', encoding='utf8') as input_file:
            for line in input_file:
                line = line.strip()
                if not line:
                    continue
                yield line

    def start_tour(self, line):
        return line.startswith('### Tour')

    def get_numb_tour(self, line):
        *_, numb_tour = line.split()
        return numb_tour

    def get_name_result(self, line):
        name, game_result = line.split('\t')
        return name, game_result

    def end_tour(self, line):
        return line.startswith('winner is')


class Tour:

    def __init__(self, numb_tour):
        self.numb_tour = numb_tour
        self.win_player = None

    def get_result_player(self, name_player, game_result):
        player = PlayerResult(name_player, game_result)
        try:
            player.get_score()
        except ValueError as exc:
            print(f'Произошла ошибка в туре {self.numb_tour}. '
                  f'Строка: {player.name_player} {player.game_result}.\n'
                  f'Ошибка: {exc}\n')
            raise
        return player

    def get_win_player(self, player):
        if self.win_player is None:
            self.win_player = player
        elif player > self.win_player:
            self.win_player = player


def main():
    tournament = TournamentBowling('tournament.txt', 'result_tournament_01.txt')
    tournament.get_result_tournament()
    tournament.print_result_tournament()


if __name__ == '__main__':
    main()


