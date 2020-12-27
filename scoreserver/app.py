#!/usr/bin/env python3
import asyncio
import logging
import os
from asyncio import sleep

import redis as redis
import requests
import random
import itertools

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
GAMESERVER_HOST = os.environ.get("GAMESERVER_HOST", "gameserver")

GAMESERVER_URL = f"http://{GAMESERVER_HOST}:5000/jsonrpc"

db = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


async def run_match(*bot_names):
    loop = asyncio.get_event_loop()

    payload = {
        "method": "run_game",
        "params": bot_names,
        "jsonrpc": "2.0",
        "id": random.randint(0, 100000),
    }
    response = await loop.run_in_executor(
        None, lambda: requests.post(GAMESERVER_URL, json=payload)
    )
    game_history = response.json()["result"]
    return game_history


async def main():
    while True:
        users = db.keys("users:*")
        for key_a, key_b in itertools.combinations(users, 2):
            user_a, user_b = db.get(key_a), db.get(key_b)
            logging.info(f"Next match: {user_a} vs {user_b}")
            game_history = await run_match("soeren", "soerface")
            logging.info("Result")
            from pprint import pprint
            pprint(game_history)
        logging.info("Sleeping, next matches will start soon")
        await sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
