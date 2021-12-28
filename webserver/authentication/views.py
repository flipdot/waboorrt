import re
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, status, Depends, HTTPException, Request, Form, Query
from redis import Redis
from sqlalchemy.orm import Session

from starlette.responses import RedirectResponse, HTMLResponse

import rc3
from constants import AUTH_TIMEOUT, SESSION_EXPIRATION_TIME, OAUTH_PROVIDERS
from dependencies import pg_session, redis_session, session_key
from .schemas import LoginResponse, LoginSchema, OAuthProvider
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
    if OAUTH_PROVIDERS["RC3"]["CLIENT_ID"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="RC3_CLIENT_ID environment variable was set. Local login is not allowed."
        )
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


@router.get("/oauth/{provider}", response_model=LoginResponse)
def login_oauth(
        code: str,
        state: str,
        provider: OAuthProvider,
        redis_db: Redis = Depends(redis_session),
        db: Session = Depends(pg_session)
):
    """
    Performs login with authentication code that was returned by the OAuth provider.
    In case of provider "local", the code will be treated as the desired username.
    """
    stored_state = redis_db.exists(f"webserver:oauth_states:{state}")

    if not stored_state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state provided")

    if provider == OAuthProvider.rc3:
        refresh_token = rc3.get_refresh_token(code)
        username = rc3.get_username(refresh_token)
        rc3_identity = username  # TODO: should we use username as rc3 identity?

        user = db.query(UserModel).filter(UserModel.rc3_identity == rc3_identity).first()
    elif provider == OAuthProvider.local:
        if OAUTH_PROVIDERS["RC3"]["CLIENT_ID"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="RC3_CLIENT_ID environment variable was set. Local login is not allowed."
            )
        username = code
        user = db.query(UserModel).filter(UserModel.username == username).first()
        rc3_identity = None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid OAuth provider")

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


@router.get("/auth-redirect", status_code=302)
def auth_redirect(request: Request, redis_db: Redis = Depends(redis_session)):
    state = uuid4()
    redis_db.set(
        f"webserver:oauth_states:{state}",
        "",
        px=AUTH_TIMEOUT,
    )
    if OAUTH_PROVIDERS["RC3"]["CLIENT_ID"]:
        url = rc3.gen_login_redirect(state)
    else:
        url = request.url_for("fake_oauth_provider") + f"?state={state}"
    return RedirectResponse(url=url)


@router.get("/fake_oauth_provider", response_class=HTMLResponse)
def fake_oauth_provider():
    """
    Non-API endpoint. Returns a simple HTML page.
    Used in local development to provide a login without an external OAuth provider.
    """
    if OAUTH_PROVIDERS["RC3"]["CLIENT_ID"]:
        return "RC3_CLIENT_ID environment variable was set. Therefore, the fake OAuth Provider is disabled."
    with open(Path("static/fake_oauth_provider.html")) as f:
        content = f.read()
    return content


@router.post("/fake_oauth_provider")
def fake_oauth_provider(request: Request, state: str, username: str = Form(...)):
    """
    Processes forms submitted by the fake OAuth Provider HTML page.
    """
    if OAUTH_PROVIDERS["RC3"]["CLIENT_ID"]:
        return "RC3_CLIENT_ID environment variable was set. Therefore, the fake OAuth Provider is disabled."
    code = username
    # Can't add extra query params due to this issue:
    # https://github.com/encode/starlette/issues/560
    # Let's use string concatenation instead ¯\_(ツ)_/¯
    url = request.url_for("index", arbitrary="oauth/local") + f"?code={code}&state={state}"
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
