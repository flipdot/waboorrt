from json import JSONEncoder
from typing import Any

from gameobjects import GameState, Bot, Action, EntityType


class GameStateEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, GameState):
            return {
                "tick": o.tick,
                "max_ticks": o.max_ticks,
                "map_w": o.map_w,
                "map_h": o.map_h,
                "entities": o.entities,
            }
        elif isinstance(o, Bot):
            return o.__dict__
        elif isinstance(o, Action):
            return o.name
        elif isinstance(o, EntityType):
            return o.name
        else:
            super(GameStateEncoder, self).default(o)
