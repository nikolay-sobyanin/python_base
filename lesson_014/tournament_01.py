from collections import defaultdict

from bowling import PlayerResult, Global, Local


class TournamentBowling:

    def __init__(self, input_file, output_file, rules):
        self.input_file = input_file
        self.output_file = output_file
        self.rules = rules
        self.parser_tour = ParserTour(self.input_file, self.rules)
        self.win_games = defaultdict(int)

    def get_result_tournament(self):
        with open(self.output_file, 'w', encoding='utf8') as output_file:
            for line in self.parser_tour.read_file():

                if self.parser_tour.is_start_tour(line):
                    tour = self.parser_tour.build_tour(line)
                    output_file.write(line + '\n')
                    continue
                elif self.parser_tour.end_tour(line):
                    self.win_games[tour.win_player.name_player] += 1
                    output_file.write(f'winner is {tour.win_player.name_player}\n\n')
                    tour = None

                if tour is not None:
                    player = self.parser_tour.get_player(line)
                    try:
                        tour.get_result_player(player)
                    except ValueError:
                        continue

                    tour.write_win_player(player)
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

    def __init__(self, input_file, rules):
        self.input_file = input_file
        self.rules = rules

    def read_file(self):
        with open(self.input_file, 'r', encoding='utf8') as input_file:
            for line in input_file:
                line = line.strip()
                if line:
                    yield line

    def is_start_tour(self, line):
        return line.startswith('### Tour')

    def build_tour(self, line):
        *_, numb_tour = line.split()
        return Tour(numb_tour)

    def get_player(self, line):
        name, game_result = line.split('\t')
        player = PlayerResult(name, game_result, self.rules())
        return player

    def end_tour(self, line):
        return line.startswith('winner is')


class Tour:

    def __init__(self, numb_tour):
        self.numb_tour = numb_tour
        self.win_player = None

    def get_result_player(self, player):
        try:
            player.compute_score()
        except ValueError as exc:
            print(f'Произошла ошибка в туре {self.numb_tour}. '
                  f'Строка: {player.name_player} {player.game_result}.\n'
                  f'Ошибка: {exc}\n')
            raise

    def write_win_player(self, player):
        if self.win_player is None or player > self.win_player:
            self.win_player = player


def main():
    tournament_local = TournamentBowling('tournament.txt', 'result_local_tournament_01.txt', rules=Local)
    tournament_local.get_result_tournament()
    tournament_local.print_result_tournament()

    tournament_external = TournamentBowling('tournament.txt', 'result_global_tournament_01.txt', rules=Global)
    tournament_external.get_result_tournament()
    tournament_external.print_result_tournament()


if __name__ == '__main__':
    main()


