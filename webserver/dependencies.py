# FastAPI dependencies explained: https://fastapi.tiangolo.com/tutorial/dependencies/
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from redis import Redis

from database import SessionLocal, redis_db
from schemas import UserSchema
from constants import SESSION_EXPIRATION_TIME


def pg_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def redis_session():
    # yield something like in pg_session?
    return redis_db


def session_key(token: str = Depends(APIKeyHeader(name="X-Session-Key"))):
    return f"webserver:session:{token}"


def current_user(
        db_session_key: str = Depends(session_key),
        cache_db: Redis = Depends(redis_session)
) -> UserSchema:
    user_id = cache_db.get(db_session_key)
    if user_id is not None:
        user_id = UUID(user_id)
        cache_db.expire(db_session_key, SESSION_EXPIRATION_TIME)
    return UserSchema(
        user_id=user_id,
        is_anonymous=user_id is None,
    )


def authentication_required(user: UserSchema = Depends(current_user)):
    if user.is_anonymous:
        raise HTTPException(status_code=403, detail="Login required")


class HasPermission:
    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self, user: UserSchema = Depends(current_user)):
        # TODO
        pass
