import re
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, status, Depends, HTTPException
from redis import Redis
from sqlalchemy.orm import Session

from starlette.responses import RedirectResponse

import rc3
from constants import AUTH_TIMEOUT, SESSION_EXPIRATION_TIME
from dependencies import pg_session, redis_session, session_key
from .schemas import LoginResponse, LoginSchema
from models import UserModel, RepositoryModel

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

def create_account(db: Session, username: str, rc3_identity: Optional[str] = None) -> UserModel:
    username = username.lower()

    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        raise ValueError("Invalid username")

    user = UserModel(username=username, rc3_identity=rc3_identity)
    repository = RepositoryModel(name=f"{username}.git", owner=user)
    db.add(user)
    db.add(repository)
    db.commit()
    db.refresh(user)
    db.refresh(repository)
    return user


@router.post("/login", response_model=LoginResponse)
def login(
        form: LoginSchema,
        db: Session = Depends(pg_session),
        redis_db: Redis = Depends(redis_session),
):
    """
    Returns session for a given username.
    If no user with the name exists, a new account will be created.
    """
    # TODO: check if rC3 is configured. If yes, don't allow this login
    user = db.query(UserModel).filter(UserModel.username == form.username).first()
    if not user:
        user = create_account(db, form.username)
    session_id = uuid4()
    redis_db.set(f"webserver:session:{session_id}", str(user.id), ex=SESSION_EXPIRATION_TIME)
    return LoginResponse(session_id=session_id)


@router.post("/logout")
def logout(
        db_session_key: str = Depends(session_key),
        redis_db: Redis = Depends(redis_session),
):
    deleted_keys = redis_db.delete(db_session_key)
    if deleted_keys <= 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return "ok"


@router.get("/rc3/login", response_model=LoginResponse)
def login_rc3(code: str, state: str, redis_db: Redis = Depends(redis_session), db: Session = Depends(pg_session)):
    stored_state = redis_db.exists(f"webserver:oauth_states:{state}")

    if not stored_state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    refresh_token = rc3.get_refresh_token(code)
    username = rc3.get_username(refresh_token)
    rc3_identity = username # TODO: should we use username as rc3 identity?

    user = db.query(UserModel).filter(UserModel.rc3_identity == rc3_identity).first()

    # create new account if required
    if user is None:
        try:
            user = create_account(db, username, rc3_identity)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    redis_db.delete(f"webserver:oauth_states:{state}")

    session_id = uuid4()
    redis_db.set(f"webserver:session:{session_id}", str(user.id), ex=SESSION_EXPIRATION_TIME)
    return LoginResponse(session_id=session_id)


@router.get("/auth-redirect", status_code=302, deprecated=True)
def auth_redirect(redis_db: Redis = Depends(redis_session),):
    state = uuid4()
    redis_db.set(
        f"webserver:oauth_states:{state}",
        "",
        px=AUTH_TIMEOUT,
    )


    return RedirectResponse(url=rc3.gen_login_redirect(state))
