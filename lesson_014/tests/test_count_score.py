import unittest
from bowling import PlayerResult


class TestCheckGameResult(unittest.TestCase):

    def setUp(self):
        self.player = PlayerResult(name_player='Nikolay', game_result=None)
        self.player.QUANTITY_FRAMES = 10

    def test_valid_symbol(self):
        self.player.game_result = 'х153/1-53-/X--62-A'
        massage_error = f'Имеются недопустимые символы. Используйте только "{self.player.GAME_SYMBOLS}".'
        with self.assertRaisesRegex(ValueError, massage_error):
            self.player.compute_score()

    def test_quantity_frames(self):
        self.player.game_result = 'х153/1-53-/X--62'
        massage_error = f'Введено неверное количество фреймов. Их должно быть {self.player.QUANTITY_FRAMES}.'
        self.assertRaisesRegex(ValueError, massage_error, self.player.compute_score)  # для практики использования данной функции

    def test_full_frames(self):
        self.player.game_result = 'х153/1-53-/X--62-'
        massage_error = f'Последний фрейм не полный.'
        with self.assertRaisesRegex(ValueError, massage_error):
            self.player.compute_score()


class TestCheckFrame(unittest.TestCase):

    def setUp(self):
        self.player = PlayerResult(name_player='Nikolay', game_result=None)

    def test_error_spare(self):
        frame = '/6'
        massage_error = f'Фрейм - "{frame}". Не может быть "Spare" при первом броске в фрейме.'
        with self.assertRaisesRegex(ValueError, massage_error):
            self.player.check_frame(frame)

    def test_error_strike(self):
        frame = '1X'
        massage_error = f'Фрейм - "{frame}". Strike может быть только при первом броске в фрейме.'
        with self.assertRaisesRegex(ValueError, massage_error):
            self.player.check_frame(frame)

    def test_error_sum_frame(self):
        frame = '56'
        massage_error = f'Фрейм - "{frame}". Сумма двух бросков не может быть больше 9.'
        with self.assertRaisesRegex(ValueError, massage_error):
            self.player.check_frame(frame)


class TestCountScore(unittest.TestCase):

    def setUp(self):
        self.player = PlayerResult(name_player='Nikolay', game_result=None)
        self.player.QUANTITY_FRAMES = 1

    def test_strike(self):
        self.player.game_result = 'X'
        self.player.compute_score()
        self.assertEqual(self.player.score, 20)

    def test_spare(self):
        self.player.game_result = '8/'
        self.player.compute_score()
        self.assertEqual(self.player.score, 15)

    def test_two_throws(self):
        self.player.game_result = '54'
        self.player.compute_score()
        self.assertEqual(self.player.score, 9)

    def test_one_throw(self):
        self.player.game_result = '-5'
        self.player.compute_score()
        self.assertEqual(self.player.score, 5)

    def test_miss(self):
        self.player.game_result = '--'
        self.player.compute_score()
        self.assertEqual(self.player.score, 0)


if __name__ == '__main__':
    unittest.main()
