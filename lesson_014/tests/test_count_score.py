import unittest
from bowling import PlayerResult


class TestCountScore(unittest.TestCase):

    def setUp(self):
        self.player = PlayerResult(name_player='Nikolay', game_result=None)
        self.player.QUANTITY_FRAMES = 1

    def test_strike(self):
        self.player.game_result = 'X'
        self.player.get_score()
        self.assertEqual(self.player.score, 20)

    def test_spare(self):
        self.player.game_result = '8/'
        self.player.get_score()
        self.assertEqual(self.player.score, 15)

    def test_two_throws(self):
        self.player.game_result = '54'
        self.player.get_score()
        self.assertEqual(self.player.score, 9)

    def test_one_throw(self):
        self.player.game_result = '-5'
        self.player.get_score()
        self.assertEqual(self.player.score, 5)

    def test_miss(self):
        self.player.game_result = '--'
        self.player.get_score()
        self.assertEqual(self.player.score, 0)


if __name__ == '__main__':
    unittest.main()
