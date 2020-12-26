from gamefunctions import tick, GameState, Action
from unittest import TestCase

WALK_NORTH = {"name": Action.WALK_NORTH}
WALK_EAST = {"name": Action.WALK_EAST}
WALK_SOUTH = {"name": Action.WALK_SOUTH}
WALK_WEST = {"name": Action.WALK_WEST}

class TestWalk(TestCase):
    def setUp(self):
        self.game_state = GameState.create()
        bots = self.game_state.bots
        bots[0].x, bots[0].y = 5, 5
        bots[1].x, bots[1].y = 25, 25

    def tearDown(self):
        pass

    def test_walk_north(self):
        game_state, _ = tick(self.game_state, (WALK_NORTH, WALK_NORTH))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 4))
        self.assertEqual((b1.x, b1.y), (25, 24))

    def test_walk_south(self):
        game_state, _ = tick(self.game_state, (WALK_SOUTH, WALK_SOUTH))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 6))
        self.assertEqual((b1.x, b1.y), (25, 26))

    def test_walk_east(self):
        game_state, _ = tick(self.game_state, (WALK_EAST, WALK_EAST))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (6, 5))
        self.assertEqual((b1.x, b1.y), (26, 25))

    def test_walk_west(self):
        game_state, _ = tick(self.game_state, (WALK_WEST, WALK_WEST))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (4, 5))
        self.assertEqual((b1.x, b1.y), (24, 25))

    def test_multiple_walks(self):
        turns = [
            (WALK_EAST, WALK_SOUTH),
            (WALK_NORTH, WALK_WEST),
            (WALK_NORTH, WALK_EAST),
            (WALK_EAST, WALK_SOUTH),
            (WALK_SOUTH, WALK_WEST),
            (WALK_SOUTH, WALK_WEST),
            (WALK_WEST, WALK_NORTH),
        ]

        game_state = self.game_state
        for actions in turns:
            game_state, _ = tick(game_state, actions)
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (6, 5))
        self.assertEqual((b1.x, b1.y), (23, 26))
