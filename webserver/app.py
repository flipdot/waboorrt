import json
import logging
import os
import subprocess
from urllib.parse import urlparse
import re

from flask import Flask, render_template, request, redirect, jsonify, abort, url_for
import redis

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

VALID_REPO_TEMPLATES = ["python"]

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


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    template = request.form.get("template")
    pubkey = request.form.get("pubkey")

    if create_user(username, template, pubkey):
        return redirect(url_for(".login_failed"))

    return redirect(url_for(".login_success", username=username))


def create_user(username, template, pubkey):
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
