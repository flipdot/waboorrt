# FastAPI dependencies explained: https://fastapi.tiangolo.com/tutorial/dependencies/
from fastapi import Header, Depends, HTTPException
from fastapi.security import APIKeyHeader

from api.int_models import UserAccount


def current_user(token: str = Depends(APIKeyHeader(name="X-API-Key"))) -> UserAccount:
    user_id = int(token or "-1")  # how about JWT?
    return UserAccount(
        user_id=user_id,
        is_anonymous=user_id < 0,
    )


def authentication_required(user: UserAccount = Depends(current_user)):
    if user.is_anonymous:
        raise HTTPException(status_code=403, detail="Login required")
