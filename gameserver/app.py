from flask.json import JSONEncoder

from flask import Flask, jsonify
from typing import Tuple, Any

from gamefunctions import tick
from gameobjects import GameState, Bot, Action, EntityType


class GameStateEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, GameState):
            return {
                "tick": o.tick,
                "max_ticks": o.max_ticks,
                "map_w": o.map_w,
                "map_h": o.map_h,
                "entities": o.entities
            }
        elif isinstance(o, Bot):
            return o.__dict__
        elif isinstance(o, Action):
            return o.name
        elif isinstance(o, EntityType):
            return o.name
        else:
            super(GameStateEncoder, self).default(o)


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
        actions: Tuple[Action, ...] = (Action.WALK_EAST, Action.WALK_EAST)
        game_state, executed_actions = tick(game_state, actions)
        game_history.append(
            {
                "game_state": game_state,
                "actions": executed_actions,
            }
        )

    return jsonify(game_history)