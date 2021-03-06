import json

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher

from typing import Tuple, Dict

from botcomms import BotCommunicator
from gamefunctions import tick
from gameobjects import GameState, Bot
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
            container_ids = [x.id[:12] for x in botcom.containers]
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
                actions: Tuple[dict, ...] = botcom.get_next_actions(game_state)
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
    return Response(
        json.dumps(response.data, cls=GameStateEncoder), mimetype="application/json"
    )


if __name__ == "__main__":
    run_simple("0.0.0.0", 5000, application, processes=8)
