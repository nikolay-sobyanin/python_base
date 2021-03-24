from abc import ABC, abstractmethod


class PlayerResult:
    QUANTITY_FRAMES = 10
    GAME_SYMBOLS = '123456789X/-'

    def __init__(self, name_player, game_result, rules):
        self.name_player = name_player
        self.game_result = game_result
        self._rules = rules
        self.score = 0

    def __str__(self):
        return f'{self.name_player:<8}{self.game_result:<24}{self.score}'

    def __gt__(self, other):
        return self.score > other.score

    def compute_score(self):
        result_list = self.get_result_list()
        self.check_result(result_list)
        self.score = self._rules.count_score(check_frame=self.check_frame, result_list=result_list)

    def get_result_list(self):
        result = self.game_result.upper().replace('Х', 'X').replace('X', 'X-')
        return [result[i:i + 2] for i in range(0, len(result), 2)]

    def check_result(self, result_list):
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

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        self._rules = rules


class BowlingRules(ABC):
    def __init__(self):
        self.score = 0

    @abstractmethod
    def count_score(self, check_frame, result_list):
        pass


class Local(BowlingRules):

    def count_score(self, check_frame, result_list):
        for frame in result_list:
            check_frame(frame)
            if frame == 'X-':
                self.score += 20
            elif frame[1] == '/':
                self.score += 15
            else:
                self.score += sum(int(i) for i in frame if i.isdigit())
        return self.score


class Global(BowlingRules):

    def __init__(self):
        super().__init__()
        self._bonus = []

    def count_score(self, check_frame, result_list):
        for i, frame in enumerate(result_list):
            check_frame(frame)
            self.computer_bonus_throws(i, frame)
            if frame == 'X-':
                self.score += 10
            elif frame[1] == '/':
                self.score += 10
            else:
                self.score += sum(int(i) for i in frame if i.isdigit())
        return self.score

    def computer_bonus_throws(self, i, frame):
        if i > 0:
            if self._bonus[i - 1] == 2:
                if frame == 'X-':
                    self.score += 10
                    self._bonus[i - 1] -= 1
                elif frame[1] == '/':
                    self.score += 10
                    self._bonus[i - 1] -= 2
                else:
                    self.score += sum(int(i) for i in frame if i.isdigit())
                    self._bonus[i - 1] -= 2
            elif self._bonus[i - 1] == 1:
                if frame == 'X-':
                    self.score += 10
                    self._bonus[i - 1] -= 1
                elif frame[0].isdigit():
                    self._bonus[i - 1] -= 1
                    self.score += int(frame[0])

            if i > 1 and self._bonus[i - 2] == 1:
                if frame == 'X-':
                    self.score += 10
                    self._bonus[i - 2] -= 1
                elif frame[0].isdigit():
                    self._bonus[i - 2] -= 1
                    self.score += int(frame[0])

        if frame == 'X-':
            self._bonus.append(2)
        elif frame[1] == '/':
            self._bonus.append(1)
        else:
            self._bonus.append(0)


def main():
    kolya = PlayerResult(name_player='Nikolay', game_result='х153/1-53-/X--62X', rules=Local())
    kolya.compute_score()
    print(kolya.game_result, kolya.get_result_list())
    print(kolya.name_player, kolya.score)

    kolya.rules = Global()
    kolya.compute_score()
    print(kolya.game_result, kolya.get_result_list())
    print(kolya.name_player, kolya.score)


if __name__ == '__main__':
    main()
