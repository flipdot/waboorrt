import os

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from constants import SQL_DATABASE_URL

redis_db = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True
)

pg_engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(bind=pg_engine)

Base = declarative_base()
