from abc import ABC, abstractmethod


class PlayerResult(ABC):

    QUANTITY_FRAMES = 10
    GAME_SYMBOLS = '123456789X/-'
    # Потому что это константы и они одинаковы для все объектов данного класса. Я сделал так сначала,
    # но я забыл как их использовать
    # через self.QUANTITY_FRAMES или через PlayerResult.QUANTITY_FRAMES

    def __init__(self, name_player, game_result):
        self.name_player = name_player
        self.game_result = game_result
        self.score = 0

    def __str__(self):
        return f'{self.name_player:<8}{self.game_result:<24}{self.score}'

    def __gt__(self, other):
        return self.score > other.score

    def compute_score(self):
        result_list = self.get_result_list()
        self.check_result(result_list)
        self.count_score(result_list)

    def get_result_list(self):
        result = self.game_result.upper().replace('Х', 'X').replace('X', 'X-')
        return [result[i:i + 2] for i in range(0, len(result), 2)]

    def check_result(self, result_list):
        #  если использовать поле self.game_result, то один из циклов можно будет убрать;
        #  self.game_result тут в исходном виде, я никак не преобразую его. И я думаю лучше оставить его так.
        #  Мало нужно будет вывести исходную запись результата и тд.
        # убедили. согласен.

        #  стоит убрать квадратные скобки. Почему стоит убрать
        #  all(i in self.GAME_SYMBOLS for frame in result_list for i in frame) - почему лучше? (а но лучше)
        #  Генератор значений получается и если встречатеся первое False, то сразу if выполняется и выкидивает искл.
        #  Не нужно весь список создавать и потом по нему заново проходить.
        #  абсолютно верно. Экономим время и память.

        if not all(i in self.GAME_SYMBOLS for frame in result_list for i in frame):
            raise ValueError(f'Имеются недопустимые символы. Используйте только "{self.GAME_SYMBOLS}".')
        elif len(result_list) != self.QUANTITY_FRAMES:
            raise ValueError(f'Введено неверное количество фреймов. Их должно быть {self.QUANTITY_FRAMES}.')
        elif len(result_list[-1]) != 2:
            raise ValueError(f'Последний фрейм не полный.')

    def check_frame(self, frame):
        if frame[0] == '/':
            raise ValueError(f'Фрейм - "{frame}". Не может быть "Spare" при первом броске в фрейме.')
        elif frame[1] == 'X':
            raise ValueError(f'Фрейм - "{frame}". Strike может быть только при первом броске в фрейме.')
        elif frame.isdigit() and sum([int(i) for i in frame]) > 9:
            raise ValueError(f'Фрейм - "{frame}". Сумма двух бросков не может быть больше 9.')

    @abstractmethod
    def count_score(self, result_list):
        pass


class LocalBowlingRules(PlayerResult):

    def count_score(self, result_list):
        for frame in result_list:
            self.check_frame(frame)

            if frame == 'X-':
                self.score += 20
            elif frame[1] == '/':
                self.score += 15
            else:
                self.score += sum(int(i) for i in frame if i.isdigit())


class ExternalBowlingRules(PlayerResult):

    def count_score(self, result_list):
        for i, frame in enumerate(result_list):
            self.check_frame(frame)

            if frame == 'X-':
                self.count_strike(i, result_list)
            elif frame[1] == '/':
                self.count_spare(i, result_list)
            else:
                self.score += sum(int(i) for i in frame if i.isdigit())

    def count_strike(self, i, result_list):
        self.score += 10
        if i == len(result_list) - 1:
            return
        if result_list[i + 1] == 'X-':
            self.score += 10
            if i == len(result_list) - 2:
                return
            if result_list[i + 2] == 'X-':
                self.score += 10
            elif result_list[i + 2][0].isdigit():
                self.score += int(result_list[i + 2][0])
        elif result_list[i + 1][1] == '/':
            self.score += 10
        else:
            self.score += sum(int(i) for i in result_list[i + 1] if i.isdigit())

    def count_spare(self, i, result_list):
        self.score += 10
        if i == len(result_list) - 1:
            return
        if result_list[i + 1] == 'X-':
            self.score += 10
        elif result_list[i + 1][0].isdigit():
            self.score += int(result_list[i + 1][0])


def main():
    kolya = LocalBowlingRules(name_player='Nikolay', game_result='х153/1-53-/X--62X')
    kolya.compute_score()
    print(kolya.game_result, kolya.get_result_list())
    print(kolya.name_player, kolya.score)

    kolya = ExternalBowlingRules(name_player='Nikolay', game_result='х153/1-53-/X--62X')
    kolya.compute_score()
    print(kolya.game_result, kolya.get_result_list())
    print(kolya.name_player, kolya.score)


if __name__ == '__main__':
    main()
