import json
import logging
import copy
from json import JSONDecodeError
from random import randint
from typing import Tuple, Optional
import requests

import docker
from docker.models.containers import Container

from gameobjects import GameState, Action, Bot, EntityType
from gamefunctions import dist
from time import sleep

from network import GameStateEncoder
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


def get_bot_view(game_state: GameState, bot_name: str):
    me: Optional[Bot] = None
    for entity in game_state.entities:
        if entity.type == EntityType.BOT:
            entity: Bot
            if entity.name == bot_name:
                me = entity
    if me is None:
        raise ValueError(f"Unknown bot {bot_name}")

    modified_game_state: GameState = copy.deepcopy(game_state)
    modified_game_state.entities = []
    visible_entities = [
        {
            "x": e.x,
            "y": e.y,
            "type": e.type,
        }
        for e in game_state.entities
        if dist((me.x, me.y), (e.x, e.y)) <= me.view_range
    ]

    view = {
        "me": {
            "x": me.x,
            "y": me.y,
            "name": me.name,
            "coins": me.coins,
            "view_range": me.view_range,
            "health": me.health,
        },
        "meta": {
            "w": game_state.map_w,
            "h": game_state.map_h,
            "tick": game_state.tick,
        },
        "entities": visible_entities,
    }
    return view


class BotCommunicator:
    """
    Starts up docker containers, each containing a gamebot,
    and talks via JSON RPC to them
    """

    def __init__(self, *bot_names):
        self.bot_names = bot_names
        self.docker_client = docker.from_env()
        self.containers = []

    def __enter__(self):
        cl = self.docker_client.containers
        self.containers = [
            cl.run(
                f"localhost/bot/{b}", auto_remove=True, network="gamenet", detach=True
            )
            for b in self.bot_names
        ]
        # give containers a chance to get up
        containers_ready = [False] * len(self.containers)
        for _ in range(30):
            for i, c in enumerate(self.containers):
                url = f"http://{c.id[:12]}:4000/jsonrpc"
                payload = {
                    "method": "health",
                    "jsonrpc": "2.0",
                    "id": randint(0, 10000),
                }
                try:
                    response = requests.post(url, json=payload, timeout=0.1).json()
                    containers_ready[i] = response.get("result")
                except requests.exceptions.RequestException:
                    logger.debug(f"Bot {c.image.tags} not yet ready")
            if all(containers_ready):
                logger.debug("All bots are ready")
                break
            sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for c in self.containers:
            c.kill()
        self.containers = []

    def get_next_actions(self, game_state: GameState) -> Tuple[dict, ...]:
        actions = []
        for container, bot in zip(self.containers, game_state.bots):
            actions.append(self.get_next_action(game_state, container, bot))
        return tuple(actions)

    def get_next_action(
        self, game_state: GameState, container: Container, bot: Bot
    ) -> dict:
        url = f"http://{container.id[:12]}:4000/jsonrpc"
        payload = {
            "method": "next_action",
            "params": get_bot_view(game_state, bot.name),
            "jsonrpc": "2.0",
            "id": randint(0, 10000),
        }
        bot.view_range = Bot.DEFAULT_VIEW_RANGE
        try:
            # logger.debug(payload)
            response = requests.post(
                url, data=json.dumps(payload, cls=GameStateEncoder), timeout=0.1,
                headers={"Content-Type": "application/json"}
            )
            # logger.debug(response)
        except requests.exceptions.Timeout:
            logger.info(f"Bot {container.image.tags} took to long to respond")
            return Action.noaction
        except requests.exceptions.RequestException:
            logger.warning(
                f"Something went very wrong while talking to bot {container.image.tags}"
            )
            return Action.noaction
        try:
            resp_data = response.json()
        except JSONDecodeError:
            logger.warning(f"Not a valid JSON response from {bot.name}: %s", response)
            return Action.noaction
        logger.debug(f"Response from bot {container.image.tags}: {response}")
        result = resp_data.get("result", Action.noaction)
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "x": {"type": "number"},
                "y": {"type": "number"},
                "range": {"type": "number"},
            }
        }
        try:
            validate(instance=result, schema=schema)
            return result
        except ValidationError:
            logger.info("Invalid client action: %s", result)
            return Action.noaction
