from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import random

from jsonrpc import JSONRPCResponseManager, dispatcher
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")


class Action:
    NOOP = "NOOP"
    WALK = "WALK"
    THROW = "THROW"
    LOOK = "LOOK"


@dispatcher.add_method
def next_action(me, meta, entities):
    logging.info(me, meta, entities)

    # ME
    # Where are we?
    x, y = me.get("x"), me.get("y")
    # How many coins do we have?
    coins = me.get("coins")
    # What is our health level?
    health = me.get("health")
    # How far can we currently look?
    # This will always be 1.0, or larger if we executed the "LOOK" action
    view_range = me.get("view_range")

    # META
    # How large is the map?
    w, h = meta.get("w"), meta.get("h")
    # Maybe also useful: Which tick do we have? The tick increases every round
    tick = meta.get("tick")

    # This is a list of all entities. You might find your opponent here!
    for entity in entities:
        x, y = entity.get("x"), entity.get("y")
        # The type is always "BOT". We may introduces obstacles later
        entity_type = entity.get("type")

    # This bot is not very smart. It will choose a random action. Look at that is possible!

    all_actions = [
        {
            "name": Action.WALK,
            "direction": random.choice(["north", "east", "south", "west"])
        },
        {
            "name": Action.THROW,
            "x": random.randint(0, w-1),
            "y": random.randint(0, h-1),
        },
        {
            "name": Action.LOOK,
            "range": random.randint(3, 10),
        }
    ]

    return random.choice(all_actions)


@dispatcher.add_method
def health():
    # This endpoint indicates that your bot is ready. Just leave it as-is
    return True


@Request.application
def application(request):
    logging.info(request)
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype="application/json")


if __name__ == "__main__":
    run_simple("0.0.0.0", 4000, application)
