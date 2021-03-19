from collections import defaultdict

from bowling import PlayerResult

# Работает, но мне не нравится как написан код, решил отправить что бы получить обратную связь и на выходных было чем
# заняться.
#
# Перое. Что за магия с разным размером табуляции в исходнои файле?! Гуглил очень много времени не нашел, как сделать.
# TODO: о каком из файлов именно идет речь?
#  конкретнее, приведите пример, если речь про tournament.txt;
#  если речь про 02_tournament.py, то жмем Ctrl + Alt + L и PyCharm причешит стиль сам.


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
# TODO: или можно один defaultdict(int).
#  А вообще можно собстенную функция скормить:
#   >>> d = defaultdict(lambda: [1,2,3])
#   >>> d[1]
#   [1, 2, 3]
#   >>> d
#   defaultdict(<function <lambda> at 0x0000026DF1A6D160>, {1: [1, 2, 3]})
#   .
#   См.TOD0 по коду.


# Четвертое. Создавать логгер для записи ошибок при расчете результата? Пока что ошибки пишу в консоль.
# TODO: нет, можно не запариваться. В 15 с логгированием поработаем + в боте прикручиваем. Тут не особо полезно,
#  т.к. всего пару сообщений в лог может идти.


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

                    # TODO: нам бы пригодилось пропускание пустых строк.

                    if line.startswith('### Tour'):
                        # TODO:
                        #  1. в split по умолчанию стоит "пробел";
                        #  2. когда приходится писать "_" несколько раз, можно использовать "*_, numb_tour"
                        _, _, numb_tour = line.split(' ')

                        # TODO: словарь... а может 2 независимых переменных? (см. следующий TOD0)
                        winner_tour = {'name': None, 'score': 0}
                        output_file.write(line + '\n')
                        tour_start = True
                        continue
                    elif line.startswith('winner is'):
                        output_file.write(f'winner is {winner_tour["name"]}\n\n')
                        tour_start = False
                        continue

                    if tour_start:
                        # TODO: вот тут же храним в переменных. Зачем выше такие же данные решили в словаре хранить?
                        name, game_result = line.split('\t')
                        # TODO: а тут вообще оказывается есть класс "результат игрока".
                        #  Так и супер. Перегрузите __lt__ у PlayerResult и тогда их можно будет сранивать между собой,
                        #  а выше сможем упростить (надеюсь додумаетесь как, пока без лишних деталей)
                        player = PlayerResult(name, game_result)
                        try:
                            player.get_score()
                        except ValueError as exc:
                            print(f'Произошла ошибка в туре {numb_tour}. Строка: {name} {game_result}.\n'
                                  f'Ошибка: {exc}\n')  # Пока что пишу в консоль. По хорошему нужно в лог ошибок писать
                            continue

                        # TODO: какой метод можно перегрузить у PlayerResult, чтобы тут стало проще?
                        output_file.write(f'{name:<8}{game_result:<24}{player.score}\n')
                        self.quantity_games[name] += 1

                        if int(player.score) > winner_tour['score']:
                            winner_tour['name'] = name
                            winner_tour['score'] = player.score
                            # TODO: думаю нам достаточно win_games. quantity_games - лишний.
                            self.win_games[name] += 1

    def print_result_tournament(self):
        for name, quantity_games in self.quantity_games.items():
            print(f'|{name:<8}|{quantity_games:^10}|{self.win_games[name]:^10}|')


tournament = TournamentBowling('tournament.txt', 'result_tournament.txt')
tournament.get_result_tournament()
tournament.print_result_tournament()

