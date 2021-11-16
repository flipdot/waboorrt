import json
import logging
import os
import subprocess
import re
from enum import Enum

import uvicorn
from flask import request, redirect, url_for
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import redis
from uuid import uuid4
import rc3
from pydantic import BaseModel

import jwt

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

# List of directories in gitserver/bot-templates
VALID_REPO_TEMPLATES = ["python", "c-sharp", "golang"]


class RepositoryTemplateName(str, Enum):
    python = "python"
    csharp = "c-sharp"
    golang = "golang"


AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "CHANGE-ME")


class UserAccount(BaseModel):
    username: str
    template: RepositoryTemplateName
    pubkey: str


# app = Flask(__name__, static_folder="static", template_folder="templates")
app = FastAPI()
db = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    """
    Serves *index.html* of the frontend from `static/webapp/index.html`
    """
    with open("static/webapp/index.html") as f:
        content = f.read()
    return content


@app.get("/api/games")
def game_list(from_id: str = "", n: int = 25):
    """
    Returns a list of past games. Can be paginated by using `from_id` and `n`
    """
    try:
        num = min(n, 25)
    except ValueError:
        raise HTTPException(status_code=400, detail="n must be int")
    if ":" in from_id:
        raise HTTPException(status_code=400, detail="colons are invalid")

    if from_id:
        from_key = f"game:{from_id}:summary"
        from_game_str = db.get(from_key)
        if not from_game_str:
            raise HTTPException(status_code=404, detail="game not found")
        from_game = json.loads(from_game_str)
        max_range = float(from_game.get("timestamp"))
    else:
        max_range = "+inf"
    game_keys = [
        f"game:{x}:summary" for x in
        db.zrevrangebyscore("matches_by_time", max_range, "-inf", start=0, num=num)
    ]
    games = [json.loads(db.get(k)) for k in game_keys]
    return games


@app.get("/api/games/{game_id}")
def game_detail(game_id: str):
    """
    Returns the logfile of the requested game
    """
    history = db.get(f"game:{game_id}:history")
    if not history:
        raise HTTPException(status_code=404)

    return json.loads(history)


@app.get("/api/templates")
def valid_repo_templates():
    """
    List of available repository templates. Used by the frontend to offer the user a list of programming
    languages to choose from. Their choice initiates a new repository which contains files from the
    corresponding template directory.
    """
    return VALID_REPO_TEMPLATES


# @app.route("/login_success/<username>")
# def login_success(username):
#     hostname = urlparse(request.base_url).hostname
#     return render_template("login_success.html", username=username, hostname=hostname)

@app.post("/users")
def login_local(user: UserAccount, response: Response):

    if create_user(user):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "Failed to create account"}

    return user


@app.get("/rc3/login")
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


AUTH_TIMEOUT = 15 * 60 * 1000


@app.get("/auth-redirect")
def auth_redirect():
    template = request.args.get("template")
    pubkey = request.args.get("pubkey")

    if template not in VALID_REPO_TEMPLATES:
        abort(400, f"invalid template: {template}")

    if not pubkey:
        abort(400, "pubkey missing")

    state = uuid4()
    db.set(
        f"webserver:oauth_states:{state}",
        json.dumps({"template": template, "pubkey": pubkey}),
        px=AUTH_TIMEOUT,
    )

    return redirect(url_for("login_local"))
    # return redirect(rc3.gen_login_redirect(state))


def create_user(user: UserAccount):
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


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
