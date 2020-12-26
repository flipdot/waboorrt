import json

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher

from typing import Tuple

from botcomms import BotCommunicator
from gamefunctions import tick
from gameobjects import GameState
import logging

from network import GameStateEncoder

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)


@dispatcher.add_method
def run_game(bot0_name: str, bot1_name: str):
    game_state = GameState.create()
    game_history = [
        {
            "game_state": game_state,
            "actions": [],
        }
    ]
    with BotCommunicator(bot0_name, bot1_name) as botcom:
        while game_state.running:
            actions: Tuple[dict, ...] = botcom.get_next_actions(game_state)
            game_state, executed_actions = tick(game_state, actions)
            game_history.append(
                {
                    "game_state": game_state,
                    "actions": executed_actions,
                }
            )
    return game_history


@Request.application
def application(request):
    if request.path == "/":
        return Response(
            '<html><pre>curl -s -X POST '
            '-H "Content-Type: application/json" '
            '-d \'{"method": "run_game", "jsonrpc": "2.0", '
            '"id": 420, "params": ["pyrandom", "pyrandom"]}\' '
            "http://localhost:5000/jsonrpc</pre>"
            "<p>replace pyrandom by name of bot</p></html>",
            mimetype="text/html",
        )
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(
        json.dumps(response.data, cls=GameStateEncoder), mimetype="application/json"
    )


if __name__ == "__main__":
    run_simple("0.0.0.0", 5000, application, processes=8)
