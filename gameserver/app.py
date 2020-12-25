from flask.json import JSONEncoder

from flask import Flask, jsonify
from typing import List, Tuple, Any
from enum import Enum, auto
import random
import copy


class Action(Enum):
    NOOP = auto()
    WALK_NORTH = auto()
    WALK_EAST = auto()
    WALK_SOUTH = auto()
    WALK_WEST = auto()


class GameState:
    def __init__(self, max_ticks=100):
        super().__init__()
        self.tick = 0
        self.max_ticks = max_ticks
        self.map_w: int = 50
        self.map_h: int = 50
        self.bots: List[Bot] = []
        self.running: bool = True

    @staticmethod
    def create(*args, **kwargs) -> "GameState":
        game_state = GameState(*args, **kwargs)

        bot0 = Bot(5, 5)
        bot1 = Bot(game_state.map_w - 5, game_state.map_h - 5)
        game_state.bots = [bot0, bot1]
        return game_state


class GameStateEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, GameState):
            return o.__dict__
        elif isinstance(o, Action):
            return o.name
        elif isinstance(o, Bot):
            return o.__dict__
        else:
            super(GameStateEncoder, self).default(o)


class Entity:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y


class Bot(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 100


app = Flask(__name__)
app.json_encoder = GameStateEncoder


@app.route("/")
def index():
    game_state = GameState.create()
    game_history = [
        {
            "game_state": game_state,
            "actions": [],
        }
    ]
    while game_state.running:
        actions: Tuple[Action, ...] = (Action.NOOP, Action.NOOP)
        game_state = tick(game_state, actions)
        game_history.append(
            {
                "game_state": game_state,
                "actions": actions,
            }
        )

    return jsonify(game_history)


def can_walk_north(state: GameState, bot: Bot) -> bool:
    new_pos = bot.y - 1
    if new_pos < 0:
        return False
    return not is_position_occupied(state, bot.x, new_pos)


def can_walk_south(state: GameState, bot: Bot) -> bool:
    new_pos = bot.y + 1
    if new_pos >= state.map_h:
        return False
    return not is_position_occupied(state, bot.x, new_pos)


def can_walk_west(state: GameState, bot: Bot) -> bool:
    new_pos = bot.x - 1
    if new_pos < 0:
        return False
    return not is_position_occupied(state, new_pos, bot.y)


def can_walk_east(state: GameState, bot: Bot) -> bool:
    new_pos = bot.x + 1
    if new_pos >= state.map_w:
        return False
    return not is_position_occupied(state, new_pos, bot.y)


def is_position_occupied(state: GameState, x: int, y: int) -> bool:
    for entity in state.bots:
        if x == entity.x and y == entity.y:
            return True
    return False


def tick(game_state: GameState, actions: Tuple[Action, ...]) -> GameState:
    if len(game_state.bots) != len(actions):
        raise ValueError("number of actions does not match number of bots")

    game_state = copy.deepcopy(game_state)
    game_state.tick += 1

    # Randomly determine which bot goes first. This makes the game more fair.
    for bot, action in random.sample(list(zip(game_state.bots, actions)), len(actions)):

        if action == Action.NOOP:
            continue

        elif action == Action.WALK_NORTH:
            bot.y -= 1 if can_walk_north(game_state, bot) else 0

        elif action == Action.WALK_EAST:
            bot.x += 1 if can_walk_east(game_state, bot) else 0

        elif action == Action.WALK_SOUTH:
            bot.y += 1 if can_walk_south(game_state, bot) else 0

        elif action == Action.WALK_WEST:
            bot.x -= 1 if can_walk_west(game_state, bot) else 0

    if game_state.tick >= game_state.max_ticks:
        game_state.running = False

    return game_state
