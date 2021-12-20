import os

import redis

db = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True
)
