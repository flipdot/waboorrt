import json
from jsonrpc.jsonrpc2 import JSONRPC20BatchResponse, JSONRPC20Response

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher

from typing import Dict

from botcomms import BotCommunicator
from gamefunctions import tick
from gameobjects import GameState
import logging

from network import GameStateEncoder

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


def get_score(game_history) -> Dict[str, float]:
    last_state: GameState = game_history[-1]["game_state"]
    bot0, bot1 = last_state.bots[0], last_state.bots[1]
    p0 = p1 = 0.5
    if bot0.health > bot1.health:
        p0 = 1
        p1 = 0
    elif bot0.health < bot1.health:
        p0 = 0
        p1 = 1
    return {
        bot0.name: p0,
        bot1.name: p1,
    }


@dispatcher.add_method
def run_game(bot0_name: str, bot1_name: str):
    game_state = GameState.create(bot0_name, bot1_name)
    game_history = [
        {
            "game_state": game_state,
            "actions": [],
        }
    ]
    score = None
    with BotCommunicator(bot0_name, bot1_name) as botcom:
        containers_ready = botcom.wait_for_container_ready()
        if not any(containers_ready):
            container_ids = [(x.id[:12] if x else None) for x in botcom.containers]
            logger.warning(f"No container (ids: {container_ids}) became ready (bots: {botcom.bot_names})")
        elif not all(containers_ready):
            score = {k: 1 for k in botcom.bot_names}
            for i, ready in enumerate(containers_ready):
                if not ready:
                    logger.info(
                        f"The bot {botcom.bot_names[i]} did not became ready. Loosing"
                    )
                    score[botcom.bot_names[i]] = 0
        else:
            while game_state.running:
                actions = botcom.get_next_actions(game_state)
                game_state, executed_actions = tick(game_state, actions)
                game_history.append(
                    {
                        "actions": executed_actions,
                        "game_state": game_state,
                    }
                )
            score = get_score(game_history)
    return {
        "history": game_history,
        "score": score,
    }


@Request.application
def application(request):
    if request.path == "/":
        return Response(
            "<html><pre>curl -s -X POST "
            '-H "Content-Type: application/json" '
            '-d \'{"method": "run_game", "jsonrpc": "2.0", '
            '"id": 420, "params": ["pyrandom", "pyrandom"]}\' '
            "http://localhost:5000/jsonrpc</pre>"
            "<p>replace pyrandom by name of bot</p></html>",
            mimetype="text/html",
        )
    response = JSONRPCResponseManager.handle(request.data, dispatcher)

    if not (isinstance(response, JSONRPC20Response) or isinstance(response, JSONRPC20BatchResponse)):
        logger.error(f"Invalid RPC response")
        return Response(status=500, response=json.dumps({"error": "Internal server error"}))

    if response.data["error"]:
        logger.warning(f"RPC Server returned error {response.data['error']}")
        return Response(
            json.dumps({"message": "RPC Server returned error"}),
            mimetype="application/json",
        )

    try:
        res_data = json.dumps(response.data, cls=GameStateEncoder)
    except TypeError as e:
        logger.error(f"Unable to encode response.data. Content: {response.data}, Exception: {e}")
        res_data = json.dumps({"message": "Internal server error (couldn't encode data)"})
    return Response(
        res_data, mimetype="application/json"
    )


if __name__ == "__main__":
    run_simple("0.0.0.0", 5000, application, processes=8)
