from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from enum import Enum, auto
import random

from jsonrpc import JSONRPCResponseManager, dispatcher
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")

class Action(Enum):
    NOOP = auto()
    WALK_NORTH = auto()
    WALK_EAST = auto()
    WALK_SOUTH = auto()
    WALK_WEST = auto()

@dispatcher.add_method
def next_action(game_state):
    logging.info(game_state)
    return random.choice(list(Action)).name

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