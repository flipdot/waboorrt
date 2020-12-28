import json
import logging
import os
import random
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, jsonify, abort
import redis
import requests

from uuid import uuid4

import jwt

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

RC3_CLIENT_ID = os.environ["RC3_CLIENT_ID"]
RC3_REDIRECT_URI = os.environ["RC3_REDIRECT_URI"]
RC3_TOKEN_URI = os.environ["RC3_TOKEN_URI"]
RC3_CLIENT_SECRET = os.environ["RC3_CLIENT_SECRET"]

AUTH_TOKEN_SECRET = os.environ["AUTH_TOKEN_SECRET"]

app = Flask(__name__, static_folder="static", template_folder="templates")
db = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)


@app.route("/")
def index():
    game_keys = sorted(db.keys("game:*:summary"))
    games = [json.loads(db.get(k)) for k in game_keys]
    # games = [
    #     {"title": "A vs B", "timestamp": datetime.now(), "id": 420},
    #     {"title": "C vs B", "timestamp": datetime.now() - timedelta(minutes=3), "id": 520},
    #     {"title": "C vs A", "timestamp": datetime.now() - timedelta(minutes=6), "id": 620},
    # ]
    return render_template("index.html", games=games)


@app.route("/game/<game_id>")
def game_history(game_id):
    history = db.get(f"game:{game_id}:history")
    if not history:
        abort(404)
    return history


def create_user():
    # TODO


@app.route("/login", methods=["POST"])
def login():
    code = request.args.get("code")
    if not code:
        return "authorization code mzissing", 400

    state = request.args.get("state")
    if not state:
        return "state missing", 400

    stored_state = db.get(f"states:{state}")
    if not stored_state or stored_state != "initialized":
        return "invalid state", 400

    r = requests.post(f"https://rc3.world/sso/token/?grant_type=authorization_code&code={code}&redirect_uri={RC3_TOKEN_URI}&client_id={RC3_CLIENT_ID}&client_secret={RC3_CLIENT_SECRET}")
    resp_data = r.json()
    if resp_data.error:
        logging.error("failed to exchange auth code for token: %s", resp_data)
        return "internal server error", 500

    user_name = "" # TODO

    user = db.get(f"users:{user_name}")
    if not user:
        create_user()

    auth_token = jwt.encode({"username": user_name}, AUTH_TOKEN_SECRET, algorithm="HS256")

    user_id = random.randint(0, 10000)  # probably we get some kind of unique stuff from oauth flow
    db.set(f"users:{user_id}", json.dumps({"botname": request.form.get("username")}))
    return redirect("/")

@app.route("/auth-redirect", methods=["GET"])
def auth_redirect():
    state = uuid4()
    db.set(f"states:{state}", "initialized")

    return redirect(f"https://rc3.world/sso/authorize?response_type=code&client_id={RC3_CLIENT_ID}&redirect_uri={RC3_REDIRECT_URI}&scopes=username&state={state}")