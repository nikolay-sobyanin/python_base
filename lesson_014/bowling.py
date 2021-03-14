
class PlayerResult:

    def __init__(self, name_player, game_result):
        self.name_player = name_player
        self.game_result = game_result
        self.score = 0
        self.QUANTITY_FRAMES = 10
        self.GAME_SYMBOLS = '123456789X/-'

    def get_score(self):
        result_list = self.get_result_list()
        self.check_result(result_list)
        for frame in result_list:
            self.check_frame(frame)
            self.count_score(frame)

    def get_result_list(self):
        result = self.game_result.replace('X', 'X-')
        return [result[i:i + 2] for i in range(0, len(result), 2)]

    def check_result(self, result_list):
        if not all([i in self.GAME_SYMBOLS for frame in result_list for i in frame]):
            raise ValueError(f'Имеются недопустимые символы. Используйте только "{self.GAME_SYMBOLS}".')
        elif len(result_list) != self.QUANTITY_FRAMES:
            raise ValueError(f'Введене неверное количество фреймов. Их должно быть {self.QUANTITY_FRAMES}.')
        elif not all([len(i) == 2 for i in result_list]):
            raise ValueError(f'Последний фрейм не полный.')

    def check_frame(self, frame):
        if frame[0] == '/':
            raise ValueError(f'Фрейм - "{frame}". Не может быть "Spare" при первом броске в фрейме.')
        elif frame[1] == 'X':
            raise ValueError(f'Фрейм - "{frame}". Strike может быть только при первом броске в фрейме.')
        elif frame.isdigit() and sum([int(i) for i in frame]) > 9:
            raise ValueError(f'Фрейм - "{frame}". Сумма двух бросков не может быть больше 9.')

    def count_score(self, frame):
        if frame == 'X-':
            self.score += 20
        elif frame[1] == '/':
            self.score += 15
        elif frame.isdigit():
            self.score += sum([int(i) for i in frame])
        elif '-' in frame:
            self.score += sum([int(i) for i in frame if i.isdigit()])


def main():
    kolya = PlayerResult(name_player='Nikolay', game_result='X153/1-53-/X--62-6')
    kolya.get_score()
    print(kolya.name_player, kolya.score)


if __name__ == '__main__':
    main()