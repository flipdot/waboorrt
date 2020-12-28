import random
from enum import Enum, auto
from typing import List


class Action:
    NOOP = "NOOP"
    WALK = "WALK"
    THROW = "THROW"
    LOOK = "LOOK"
    noaction = {"name": NOOP}


class EntityType(Enum):
    ENTITY = auto()
    BOT = auto()


# class BotView:
#     """
#     Represents the object that gets send to the bots
#     """
#
#     def __init__(self):
#


class GameState:
    def __init__(self, max_ticks=100):
        self.tick = 0
        self.max_ticks = max_ticks
        self.map_w: int = 16
        self.map_h: int = 16
        self.bots: List[Bot] = []
        self.entities: List[Entity] = []
        self.running: bool = True

    @staticmethod
    def create(bot0_name="0", bot1_name="1", *args, **kwargs) -> "GameState":
        game_state = GameState(*args, **kwargs)

        margin = 1

        def rndw() -> int:
            return random.randint(margin, game_state.map_w - 1 - margin)

        def rndh() -> int:
            return random.randint(margin, game_state.map_h - 1 - margin)

        bot0 = Bot(bot0_name, rndw(), rndh())
        bot1 = Bot(bot1_name, rndw(), rndh())
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
        self.type: EntityType = EntityType.BOT
        self.health: int = 100
        self.name: str = name
        self.coins: int = 42
        self.view_range: float = 1.0
