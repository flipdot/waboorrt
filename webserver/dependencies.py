# FastAPI dependencies explained: https://fastapi.tiangolo.com/tutorial/dependencies/
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import UserSchema
from models import UserModel


def pg_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(
        token: str = Depends(APIKeyHeader(name="X-API-Key")),
        db: Session = Depends(pg_session),
) -> UserSchema:
    user_id = int(token or "-1")
    user = db.query(UserModel).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return UserSchema(
        user_id=user_id,
        user=user,
        is_anonymous=user_id < 0,
    )


def authentication_required(user: UserSchema = Depends(current_user)):
    if user.is_anonymous:
        raise HTTPException(status_code=403, detail="Login required")
