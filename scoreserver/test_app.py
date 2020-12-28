from unittest import TestCase
from app import calculate_new_elo_ranking


class TestApp(TestCase):
    def test_elo_ranking_first_wins(self):
        old_r0, old_r1 = 2806, 2577
        r0, r1 = calculate_new_elo_ranking((old_r0, old_r1), (0, 1), k=10)
        self.assertEqual(r0, 2798)
        self.assertEqual(r1, 2585)

    def test_elo_ranking_second_wins(self):
        old_r0, old_r1 = 2806, 2577
        r0, r1 = calculate_new_elo_ranking((old_r0, old_r1), (1, 0), k=10)
        self.assertEqual(r0, 2808)
        self.assertEqual(r1, 2575)

    def test_elo_ranking_draw(self):
        old_r0, old_r1 = 2806, 2577
        r0, r1 = calculate_new_elo_ranking((old_r0, old_r1), (0.5, 0.5), k=10)
        self.assertEqual(r0, 2803)
        self.assertEqual(r1, 2580)
