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


class TestThrow(TestCase):
    def setUp(self):
        self.game_state = GameState.create()
        bots = self.game_state.bots
        bots[0].x, bots[0].y = 5, 5
        bots[1].x, bots[1].y = 25, 25

    def tearDown(self):
        pass

    def test_throw_oob(self):
        game_state, _ = tick(self.game_state, (
            {"name": Action.THROW, "x": -10, "y": -10},
            {"name": Action.THROW, "x": 100, "y": 100}
        ))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 5))
        self.assertEqual((b1.x, b1.y), (25, 25))
        self.assertEqual(b0.health, 100)
        self.assertEqual(b1.health, 100)

    def test_throw_center(self):
        game_state, _ = tick(self.game_state, (
            {"name": Action.THROW, "x": 12, "y": 12},
            {"name": Action.THROW, "x": 13, "y": 13}
        ))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 5))
        self.assertEqual((b1.x, b1.y), (25, 25))
        self.assertEqual(b0.health, 100)
        self.assertEqual(b1.health, 100)

    def test_throw_directly(self):
        game_state, _ = tick(self.game_state, (
            {"name": Action.THROW},  # should default to (5,5)
            {"name": Action.THROW, "x": 5, "y": 5}
        ))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 5))
        self.assertEqual((b1.x, b1.y), (25, 25))
        self.assertEqual(b0.health, 80)  # 100-10-10
        self.assertEqual(b1.health, 100)

    def test_throw_close(self):
        game_state, _ = tick(self.game_state, (
            {"name": Action.THROW, "x": 5, "y": 4},
            {"name": Action.THROW, "x": 6, "y": 6}
        ))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 5))
        self.assertEqual((b1.x, b1.y), (25, 25))
        self.assertEqual(b0.health, 87)  # 87=100-damage(1)-damage(sqrt(2))=100-7-6
        self.assertEqual(b1.health, 100)
