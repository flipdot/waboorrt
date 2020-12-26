import json
import logging
from random import randint
from typing import Tuple
import requests

import docker
from docker.models.containers import Container

from gameobjects import GameState, Action
from time import sleep

from network import GameStateEncoder
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


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
                logger.info("All bots are ready")
                break
            sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for c in self.containers:
            c.kill()
        self.containers = []

    def get_next_actions(self, game_state: GameState) -> Tuple[dict, ...]:
        actions = []
        for container in self.containers:
            actions.append(self.get_next_action(game_state, container))
        return tuple(actions)

    def get_next_action(self, game_state: GameState, container: Container) -> dict:
        url = f"http://{container.id[:12]}:4000/jsonrpc"
        payload = {
            "method": "next_action",
            "params": {
                # TODO: do not send whole state, just stuff the bot can see
                "game_state": game_state,
            },
            "jsonrpc": "2.0",
            "id": randint(0, 10000),
        }
        try:
            response = requests.post(
                url, data=json.dumps(payload, cls=GameStateEncoder), timeout=0.1
            ).json()
        except requests.exceptions.Timeout:
            logger.info(f"Bot {container.image.tags} took to long to respond")
            return Action.noaction
        except requests.exceptions.RequestException:
            logger.warning(
                f"Something went very wrong while talking to bot {container.image.tags}"
            )
            return Action.noaction
        logger.debug(f"Response from bot {container.image.tags}: {response}")
        result = response.get("result", Action.noaction)
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            "required": ["name"],
        }
        try:
            validate(instance=result, schema=schema)
            return result
        except ValidationError:
            return Action.noaction
