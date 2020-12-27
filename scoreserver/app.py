#!/usr/bin/env python3
import asyncio
import functools
import logging

import requests
import random

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

GAMESERVER_URL = "http://gameserver:5000/jsonrpc"


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
    game_history = await run_match("soeren", "soerface")


if __name__ == '__main__':
    asyncio.run(main())
