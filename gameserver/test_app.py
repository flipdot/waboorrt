from app import tick, GameState, Action
from unittest import TestCase

class TestWalk(TestCase):

    def setUp(self):
        self.game_state = GameState.create()
        bots = self.game_state.bots
        bots[0].x, bots[0].y = 5, 5
        bots[1].x, bots[1].y = 25, 25

    def tearDown(self):
        pass

    def test_walk_north(self):
        game_state = tick(self.game_state, (Action.WALK_NORTH, Action.WALK_NORTH))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 4))
        self.assertEqual((b1.x, b1.y), (25, 24))

    def test_walk_south(self):
        game_state = tick(self.game_state, (Action.WALK_SOUTH, Action.WALK_SOUTH))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (5, 6))
        self.assertEqual((b1.x, b1.y), (25, 26))

    def test_walk_east(self):
        game_state = tick(self.game_state, (Action.WALK_EAST, Action.WALK_EAST))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (6, 5))
        self.assertEqual((b1.x, b1.y), (26, 25))

    def test_walk_west(self):
        game_state = tick(self.game_state, (Action.WALK_WEST, Action.WALK_WEST))
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (4, 5))
        self.assertEqual((b1.x, b1.y), (24, 25))

    def test_multiple_walks(self):
        turns = [
            (Action.WALK_EAST, Action.WALK_SOUTH),
            (Action.WALK_NORTH, Action.WALK_WEST),
            (Action.WALK_NORTH, Action.WALK_EAST),
            (Action.WALK_EAST, Action.WALK_SOUTH),
            (Action.WALK_SOUTH, Action.WALK_WEST),
            (Action.WALK_SOUTH, Action.WALK_WEST),
            (Action.WALK_WEST, Action.WALK_NORTH),
        ]

        
        game_state = self.game_state
        for actions in turns:
            game_state = tick(game_state, actions)
        b0, b1 = game_state.bots
        self.assertEqual((b0.x, b0.y), (6, 5))
        self.assertEqual((b1.x, b1.y), (23, 26))
