import json
import re
import subprocess
from uuid import uuid4

import jwt
from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import RedirectResponse

import rc3
from constants import AUTH_TIMEOUT, AUTH_TOKEN_SECRET
from database import db
from api.req_models import LegacyUserAccount

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {
        "access_token": 5,
        "token_type": "bearer",
    }

# @app.route("/login_success/<username>")
# def login_success(username):
#     hostname = urlparse(request.base_url).hostname
#     return render_template("login_success.html", username=username, hostname=hostname)


@router.post("/users", deprecated=True)
def login_local(user: LegacyUserAccount, response: Response):

    if create_user(user):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "Failed to create account"}

    return user


@router.get("/rc3/login", deprecated=True)
def login_rc3():
    if "code" not in request.args:
        abort(400, "authorization code missing")
    if "state" not in request.args:
        abort(400, "state missing")

    code = request.args["code"]
    state = request.args["state"]

    stored_state = db.get(f"webserver:oauth_states:{state}")

    if not stored_state:
        abort(400, "invalid state")

    refresh_token = rc3.get_refresh_token(code)
    username = rc3.get_username(refresh_token)

    stored_state = json.loads(stored_state)

    if create_user(username, stored_state["template"], stored_state["pubkey"]):
        return redirect(url_for(".login_failed"))

    auth_token = jwt.encode(
        {"username": username}, AUTH_TOKEN_SECRET, algorithm="HS256"
    )

    db.delete(f"webserver:oauth_states:{state}")

    return redirect(f"/?login_success={username}")


@router.get("/auth-redirect", status_code=302, deprecated=True)
def auth_redirect(template: str, pubkey: str):
    # if template not in VALID_REPO_TEMPLATES:
    #     abort(400, f"invalid template: {template}")

    # if not pubkey:
    #     abort(400, "pubkey missing")

    state = uuid4()
    db.set(
        f"webserver:oauth_states:{state}",
        json.dumps({"template": template, "pubkey": pubkey}),
        px=AUTH_TIMEOUT,
    )

    return RedirectResponse(url="/login_local")
    # return redirect(rc3.gen_login_redirect(state))


def create_user(user: LegacyUserAccount):
    # TODO those checks can probably be done with pydantic in an elegant way

    # Remove everything after the second space. Discards comments from ssh keys
    pubkey = " ".join(user.pubkey.split(" ")[:2])

    if not re.match(r"^[a-zA-Z0-9_-]+$", user.username):
        raise ValueError("Invalid username")
    if not re.match(r"^[a-zA-Z0-9+=/@ -]+$", pubkey):
        raise ValueError("Invalid ssh public key")

    completed_process = subprocess.run(
        ["ssh", "root@gitserver", "newbot", f'"{user.username}" "{user.template}" "{pubkey}"']
    )
    return completed_process.returncode