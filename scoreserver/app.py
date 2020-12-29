#!/usr/bin/env python3
import asyncio
from datetime import datetime
import json
import logging
import os
from asyncio import sleep
from json import JSONDecodeError
from typing import Dict, Tuple
from uuid import uuid1

import redis as redis
import requests
import random
import itertools

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

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
    try:
        game_history = response.json().get("result")
    except JSONDecodeError:
        logger.error(f"could not decode json response from gameserver (bots: {bot_names}")
        return None
    if not game_history:
        logger.error("invalid response from gameserver")
        return None
    return game_history


def get_score(game_history) -> Dict[str, float]:
    last_state = game_history[-1]["game_state"]
    bot0, bot1 = [x for x in last_state["entities"] if x["type"] == "BOT"]
    p0 = p1 = 0.5
    if bot0["health"] > bot1["health"]:
        p0 = 1
        p1 = 0
    elif bot0["health"] < bot1["health"]:
        p0 = 0
        p1 = 1
    return {
        bot0["name"]: p0,
        bot1["name"]: p1,
    }


def calculate_new_elo_ranking(
    current_rank: Tuple[int, int], points: Tuple[float, float], k=20
) -> Tuple[int, int]:
    """Get new ELO rating. Formula implemented from https://de.wikipedia.org/wiki/Elo-Zahl

    current_rank is a tuple with ELO ranking from both players.
    points is a tuple, which may be (1, 0) for first player won,
    (0, 1) for second player won, (0.5, 0.5) for draw"""
    # current ranks
    r0, r1 = current_rank
    rdiff = max(min(r1 - r0, 400), -400)  # rdiff in [-400, 400]
    # expected values
    e0 = 1 / (1 + 10 ** (rdiff / 400))
    e1 = 1 / (1 + 10 ** (-rdiff / 400))
    new_r0 = round(r0 + k * (points[0] - e0))
    new_r1 = round(r1 + k * (points[1] - e1))
    return new_r0, new_r1


async def main():
    while True:
        users = db.keys("user:*")
        for key_a, key_b in itertools.combinations(users, 2):
            user_a, user_b = json.loads(db.get(key_a)), json.loads(db.get(key_b))
            bot_a_name, bot_b_name = user_a["botname"], user_b["botname"]
            logging.debug(f"Next match: {bot_a_name} vs {bot_b_name}")
            # TODO: maybe parallelize it. gameserver can handle multiple requests
            game_history = await run_match(bot_a_name, bot_b_name)
            if not game_history:
                continue
            score = get_score(game_history)
            bot_a_old_rank = user_a.get("elo_rank", 1200)
            bot_b_old_rank = user_b.get("elo_rank", 1200)
            bot_a_new_rank, bot_b_new_rank = calculate_new_elo_ranking(
                (bot_a_old_rank, bot_b_old_rank),
                (
                    score[bot_a_name],
                    score[bot_b_name],
                ),
            )
            rankdiff_a = bot_a_new_rank - bot_a_old_rank
            rankdiff_b = bot_b_new_rank - bot_b_old_rank
            user_a["elo_rank"] = bot_a_new_rank
            user_b["elo_rank"] = bot_b_new_rank
            game_result = {
                "id": str(uuid1()),
                "title": f"{bot_a_name} vs {bot_b_name}",
                "timestamp": datetime.now().timestamp(),
                "scores": score,
                "elo_rank": {
                    bot_a_name: bot_a_new_rank,
                    bot_b_name: bot_b_new_rank,
                },
            }
            logging.info(
                "Match done, new rankings: "
                f"{bot_a_name}: {user_a['elo_rank']} ({rankdiff_a:+}), "
                f"{bot_b_name}: {user_b['elo_rank']} ({rankdiff_b:+})"
            )
            db.set(f"game:{game_result['id']}:summary", json.dumps(game_result))
            db.set(f"game:{game_result['id']}:history", json.dumps(game_history))
            db.zadd(
                "matches_by_time", {f"{game_result['id']}": game_result["timestamp"]}
            )
            db.set(key_a, json.dumps(user_a))
            db.set(key_b, json.dumps(user_b))
        logging.info("Sleeping, next matches will start soon")
        await sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
