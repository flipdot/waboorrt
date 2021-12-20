# FastAPI dependencies explained: https://fastapi.tiangolo.com/tutorial/dependencies/
from fastapi import Header, Depends, HTTPException

from api.int_models import UserAccount


def current_user(x_token: str = Header("")) -> UserAccount:
    user_id = int(x_token or "-1")  # how about JWT?
    return UserAccount(
        user_id=user_id,
        is_anonymous=user_id < 0,
    )


def authentication_required(user: UserAccount = Depends(current_user)):
    if user.is_anonymous:
        raise HTTPException(status_code=403, detail="Login required")
