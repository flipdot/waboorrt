# FastAPI dependencies explained: https://fastapi.tiangolo.com/tutorial/dependencies/
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from redis import Redis
from sqlalchemy.orm import Session

from database import SessionLocal, redis_db
from models import APIKeyModel
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


def session_key(bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = bearer.credentials
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Login required")


def api_authentication_required(
        raw_token: str = Depends(APIKeyHeader(name="X-API-Key")),
        db: Session = Depends(pg_session)
):
    try:
        token = UUID(raw_token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
    key_exists = db.query(db.query(APIKeyModel).filter(APIKeyModel.id == token).exists()).scalar()
    if not key_exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown API Key")


class HasPermission:
    def __init__(self, permission: str):
        self.permission = permission

    def __call__(self, user: UserSchema = Depends(current_user)):
        # TODO
        pass
