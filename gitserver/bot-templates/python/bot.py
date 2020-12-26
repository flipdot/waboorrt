from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from enum import Enum, auto
import random

from jsonrpc import JSONRPCResponseManager, dispatcher
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

class Action:
    NOOP = "NOOP"
    WALK_NORTH = "WALK_NORTH"
    WALK_EAST = "WALK_EAST"
    WALK_SOUTH = "WALK_SOUTH"
    WALK_WEST = "WALK_WEST"
    THROW = "THROW"

@dispatcher.add_method
def next_action(game_state):
    logging.info(game_state)
    return random.choice([
        {
            "name": random.choice([
                Action.NOOP,
                Action.WALK_NORTH,
                Action.WALK_EAST,
                Action.WALK_SOUTH,
                Action.WALK_WEST,
            ])
        },
        {
            "name": Action.THROW,
            "x": random.randint(0, 50 - 1),
            "y": random.randint(0, 50 - 1),
        },
    ])


@dispatcher.add_method
def health():
    return True


@Request.application
def application(request):
    logging.info(request)
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype="application/json")


if __name__ == "__main__":
    run_simple("0.0.0.0", 4000, application)