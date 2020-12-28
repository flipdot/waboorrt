import json
import logging
import os
import subprocess
from urllib.parse import urlparse
import re

import requests
from flask import Flask, render_template, request, redirect, jsonify, abort, url_for
import redis

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

VALID_REPO_TEMPLATES = ["python"]

RC3_CLIENT_ID = os.environ["RC3_CLIENT_ID"]
RC3_REDIRECT_URI = os.environ["RC3_REDIRECT_URI"]
RC3_TOKEN_URI = os.environ["RC3_TOKEN_URI"]
RC3_CLIENT_SECRET = os.environ["RC3_CLIENT_SECRET"]
AUTH_TOKEN_SECRET = os.environ["AUTH_TOKEN_SECRET"]

app = Flask(__name__, static_folder="static", template_folder="templates")
db = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)


@app.route("/")
def index():
    game_keys = [f"game:{x}:summary" for x in db.zrevrangebyscore("matches_by_time", "+inf", "-inf", start=0, num=25)]
    logging.debug(f"game_keys: {game_keys}")
    # game_keys = sorted(db.keys("game:*:summary"))
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


@app.route("/login/rc3", methods=["POST"])
def login_rc3():
    if "code" not in request.args:
        abort(400, "authorization code missing")
    if "state" not in request.args:
        abort(400, "state missing")

    code = request.args["code"]
    state = request.args["state"]
    # TODO: what is that state?
    stored_state = db.get(f"webserver:state:{state}")

    username = "OAUTH"
    template = VALID_REPO_TEMPLATES[0]  # user should be able to choose
    pubkey = "ssh-rsa AAAAA"

    resp = requests.post(
        f"https://rc3.world/sso/token/"
        f"?grant_type=authorization_code"
        f"&code={code}"
        f"&redirect_uri={RC3_TOKEN_URI}"
        f"&client_id={RC3_CLIENT_ID}"
        f"&client_secret={RC3_CLIENT_SECRET}")

    resp_data = resp.json()
    if resp_data.error:
        logging.error("failed to exchange auth code for token: %s", resp_data)
        abort(500)

    if create_user(username, template, pubkey):
        return redirect(url_for(".login_failed"))

    return redirect(url_for(".login_success", username=username))


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
        abort(400, description=f"Invalid template, please choose from {VALID_REPO_TEMPLATES}")

    completed_process = subprocess.run(["ssh", "root@gitserver", "newbot", f'"{username}" "{template}" "{pubkey}"'])
    return completed_process.returncode
