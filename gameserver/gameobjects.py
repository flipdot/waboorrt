import random
from enum import Enum, auto
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


class ActionName(str, Enum):
    NOOP = "noop"
    WALK = "walk"
    THROW = "throw"
    LOOK = "look"
    CHARGE = "charge"


class RpcAction(BaseModel):
    name: ActionName


class NoopAction(RpcAction):
    name: Literal[ActionName.NOOP] = ActionName.NOOP


class ChargeAction(RpcAction):
    name: Literal[ActionName.CHARGE] = ActionName.CHARGE


class WalkAction(RpcAction):
    name: Literal[ActionName.WALK] = ActionName.WALK
    direction: str


class ThrowAction(RpcAction):
    name: Literal[ActionName.THROW] = ActionName.THROW
    x: int
    y: int


class LookAction(RpcAction):
    name: Literal[ActionName.LOOK] = ActionName.LOOK
    range: int


action_name_map: Dict[ActionName, Any] = {
    ActionName.NOOP: NoopAction,
    ActionName.WALK: WalkAction,
    ActionName.THROW: ThrowAction,
    ActionName.LOOK: LookAction,
    ActionName.CHARGE: ChargeAction,
}


class EntityType(Enum):
    ENTITY = auto()
    BOT = auto()


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

        def rnd_x() -> int:
            return random.randint(margin, game_state.map_w - 1 - margin)

        def rnd_y() -> int:
            return random.randint(margin, game_state.map_h - 1 - margin)

        bot0 = Bot(bot0_name, rnd_x(), rnd_y())
        bot1 = Bot(bot1_name, rnd_x(), rnd_y())
        game_state.bots = [bot0, bot1]
        game_state.entities = [bot0, bot1]
        return game_state


class Entity:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y
        self.type: EntityType = EntityType.ENTITY


class Bot(Entity):

    DEFAULT_VIEW_RANGE = 1.0

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type: EntityType = EntityType.BOT
        self.health: int = 100
        self.name: str = name
        self.energy: int = 5
        self.view_range: float = Bot.DEFAULT_VIEW_RANGE
