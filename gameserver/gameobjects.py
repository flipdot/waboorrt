from enum import Enum, auto
from typing import List

class Action:
    NOOP = "NOOP"
    WALK_NORTH = "WALK_NORTH"
    WALK_EAST = "WALK_EAST"
    WALK_SOUTH = "WALK_SOUTH"
    WALK_WEST = "WALK_WEST"
    THROW = "THROW"
    noaction = {"name": NOOP}

class EntityType(Enum):
    ENTITY = auto()
    BOT = auto()


class GameState:
    def __init__(self, max_ticks=100):
        super().__init__()
        self.tick = 0
        self.max_ticks = max_ticks
        self.map_w: int = 50
        self.map_h: int = 50
        self.bots: List[Bot] = []
        self.entities: List[Entity] = []
        self.running: bool = True

    @staticmethod
    def create(*args, **kwargs) -> "GameState":
        game_state = GameState(*args, **kwargs)

        bot0 = Bot("0", 5, 5)
        bot1 = Bot("1", game_state.map_w - 5, game_state.map_h - 5)
        game_state.bots = [bot0, bot1]
        game_state.entities = [bot0, bot1]
        return game_state


class Entity:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y
        self.type: EntityType = EntityType.ENTITY


class Bot(Entity):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = EntityType.BOT
        self.health = 100
        self.name = name
