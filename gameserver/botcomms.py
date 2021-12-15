import json
import logging
import copy
from json import JSONDecodeError
from random import randint
from typing import Tuple, Optional
from pydantic.tools import parse_obj_as
import requests
from signal import signal, SIGTERM, SIGKILL, SIGINT
import sys

import docker
import docker.errors
from docker.models.containers import Container

from gameobjects import GameState, Bot, RpcAction, NoopAction, action_name_map
from gamefunctions import dist
from time import sleep

from network import GameStateEncoder
from pydantic import ValidationError

import hashlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_bot_view(game_state: GameState, bot_name: str):
    me: Optional[Bot] = None
    for entity in game_state.entities:
        if isinstance(entity, Bot):
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


def get_bot_image_name(bot_name):
    hasher = hashlib.sha1()
    hasher.update(bot_name.encode())

    return f"localhost/bot/{hasher.hexdigest()[:32]}"


class BotCommunicator:
    """
    Starts up docker containers, each containing a gamebot,
    and talks via JSON RPC to them
    """

    def __init__(self, *bot_names):
        self.bot_names = bot_names
        self.docker_client = docker.from_env()
        self.containers = []
        self.containers_ready = []

    def __enter__(self):
        # signal(SIGTERM, self._sigint_handler)
        # signal(SIGINT, self._sigint_handler)
        cl = self.docker_client.containers
        self.containers_ready = [False] * len(self.bot_names)
        self.containers = []
        for bot_name in self.bot_names:
            try:
                container = cl.run(
                    get_bot_image_name(bot_name),
                    auto_remove=True,
                    network="gamenet",
                    detach=True
                )
            except docker.errors.APIError as e:
                logger.error(f"Could not start container for {bot_name}: %s", e)
                container = None
            self.containers.append(container)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("BotCommunicator: __exit__")
        self._kill_containers()

    def _sigint_handler(self, signal_received, frame):
        logger.info('Ctrl + C handler called')

        self.__exit__(None, None, None)
        sys.exit(0)

    def _kill_containers(self):
        for c in self.containers:
            if c is not None:
                c.kill()
        self.containers = []

    def wait_for_container_ready(self):
        for _ in range(30):
            for i, c in enumerate(self.containers):
                if c is None:
                    continue
                url = f"http://{c.id[:12]}:4000/jsonrpc"
                payload = {
                    "method": "health",
                    "jsonrpc": "2.0",
                    "id": randint(0, 10000),
                }
                try:
                    response = requests.post(url, json=payload, timeout=0.1).json()
                    self.containers_ready[i] = response.get("result")
                except requests.exceptions.RequestException as e:
                    logger.debug(f"Bot {c.image.tags} not yet ready: {e}")
            if all(self.containers_ready):
                logger.debug("All bots are ready")
                break
            sleep(0.1)
        return self.containers_ready

    def get_next_actions(self, game_state: GameState) -> Tuple[RpcAction, ...]:
        actions = []
        for container, bot in zip(self.containers, game_state.bots):
            actions.append(self.get_next_action(game_state, container, bot))
        return tuple(actions)

    def get_next_action(
        self, game_state: GameState, container: Container, bot: Bot
    ) -> RpcAction:
        if container.id is None or container.image is None:
            raise ValueError("container has no id or image")

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
            return NoopAction()
        except requests.exceptions.RequestException:
            logger.warning(
                f"Something went very wrong while talking to bot {container.image.tags}"
            )
            return NoopAction()

        try:
            resp_data = response.json()
        except JSONDecodeError:
            logger.warning(f"Not a valid JSON response from {bot.name}: %s", response)
            return NoopAction()

        logger.debug(f"Response from bot {container.image.tags}: {response}")
        result = resp_data.get("result")

        if result is None:
            logger.warning(f"No result from bot {container.image.tags}")
            return NoopAction()

        result['name'] = result['name'].lower()

        if result['name'] not in action_name_map:
            logger.warning(f"Unknown action type {result['name']}")
            return NoopAction()

        try:
            action = parse_obj_as(action_name_map[result['name']], result)
            return action
        except ValidationError:
            logger.info("Invalid client action: %s", result)
            return NoopAction()
