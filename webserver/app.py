import json
import logging
import os
import subprocess
import re

import uvicorn
from flask import render_template, request, redirect, jsonify, url_for, Response
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import redis
from uuid import uuid4
import rc3

import jwt

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

VALID_REPO_TEMPLATES = ["python", "c-sharp", "golang"]


AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET", "CHANGE-ME")

# app = Flask(__name__, static_folder="static", template_folder="templates")
app = FastAPI()
db = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/webapp/index.html") as f:
        content = f.read()
    return content


@app.get("/api/games")
def game_list(from_id: str = "", n: int = 25):
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
def games_list(game_id: int):
    history = db.get(f"game:{game_id}:history")
    if not history:
        raise HTTPException(status_code=404)

    return Response(history, mimetype='application/json')


@app.get("/api/templates")
def valid_repo_templates():
    return VALID_REPO_TEMPLATES


# @app.route("/login_success/<username>")
# def login_success(username):
#     hostname = urlparse(request.base_url).hostname
#     return render_template("login_success.html", username=username, hostname=hostname)


@app.get("/login_failed")
def login_failed():
    return render_template("login_failed.html")


@app.post("/login/local")
def login_local():
    username = request.form.get("username")
    template = request.form.get("template")
    pubkey = request.form.get("pubkey")

    if create_user(username, template, pubkey):
        return redirect(url_for(".login_failed"))

    return redirect(url_for(".login_success", username=username))


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


def create_user(username, template, pubkey):
    # Remove everything after the second space. Discards comments from ssh keys
    pubkey = " ".join(pubkey.split(" ")[:2])
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        abort(400, description="Invalid username")
        return "Invalid username", 400
    if not re.match(r"^[a-zA-Z0-9+=/@ -]+$", pubkey):
        abort(400, description="Invalid ssh public key")
        return "Invalid ssh public key", 400
    if template not in VALID_REPO_TEMPLATES:
        abort(
            400,
            description=f"Invalid template, please choose from {VALID_REPO_TEMPLATES}",
        )

    completed_process = subprocess.run(
        ["ssh", "root@gitserver", "newbot", f'"{username}" "{template}" "{pubkey}"']
    )
    return completed_process.returncode


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
