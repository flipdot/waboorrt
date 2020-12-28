import json
import logging
import os
import subprocess
from urllib.parse import urlparse
import re


from flask import Flask, render_template, request, redirect, jsonify, abort, url_for, Response, current_app
import redis
from uuid import uuid4
import rc3

import jwt

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

VALID_REPO_TEMPLATES = ["python"]


AUTH_TOKEN_SECRET = os.environ["AUTH_TOKEN_SECRET"]

app = Flask(__name__, static_folder="static", template_folder="templates")
db = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True
)


@app.route("/")
def index():
    return current_app.send_static_file('/webapp/index.html')


@app.route("/api/games")
def game_list():
    from_id = request.args.get("from", "")
    try:
        num = min(int(request.args.get("n", 25)), 25)
    except ValueError:
        abort(400, description="n must be int")
        return  # return is only for better ide linting ("num may not be defined")
    if ":" in from_id:
        abort(400, description="colons are invalid")

    if from_id:
        from_key = f"game:{from_id}:summary"
        from_game_str = db.get(from_key)
        if not from_game_str:
            abort(404, description="game not found")
        from_game = json.loads(from_game_str)
        max_range = float(from_game.get("timestamp"))
    else:
        max_range = "+inf"
    game_keys = [
        f"game:{x}:summary" for x in
        db.zrevrangebyscore("matches_by_time", max_range, "-inf", start=0, num=num)
    ]
    games = [json.loads(db.get(k)) for k in game_keys]
    return jsonify(games)


@app.route("/api/templates")
def valid_repo_templates():
    return jsonify(VALID_REPO_TEMPLATES)


@app.route("/api/games/<game_id>")
def game_history(game_id):
    history = db.get(f"game:{game_id}:history")
    if not history:
        abort(404)

    return Response(history, mimetype='application/json')


@app.route("/login_success/<username>")
def login_success(username):
    hostname = urlparse(request.base_url).hostname
    return render_template("login_success.html", username=username, hostname=hostname)


@app.route("/login_failed")
def login_failed():
    return render_template("login_failed.html")


@app.route("/login/local", methods=["POST"])
def login_local():
    username = request.form.get("username")
    template = request.form.get("template")
    pubkey = request.form.get("pubkey")

    if create_user(username, template, pubkey):
        return redirect(url_for(".login_failed"))

    return redirect(url_for(".login_success", username=username))


@app.route("/rc3/login", methods=["GET"])
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

    return redirect(url_for(".login_success", username=username, auth_token=auth_token))


AUTH_TIMEOUT = 15 * 60 * 1000


@app.route("/auth-redirect", methods=["GET"])
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

    return redirect(rc3.gen_login_redirect(state))


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
