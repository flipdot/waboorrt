import json
import logging
import os
import random
import subprocess
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, jsonify, abort
import redis

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

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


@app.route("/login", methods=["POST"])
def login():
    # TODO: validate with regex
    # ^[a-zA-Z0-9_-]+
    username = request.form.get("username")
    # TODO: limit to certain options (bot-templates/*
    template = request.form.get("template")
    # TODO: validate with regex
    # ^[a-zA-Z0-9+=/ -]+$
    pubkey = request.form.get("pubkey")
    # TODO: IS THIS REALLY SECURE?!
    subprocess.run(["ssh", "root@gitserver", "newbot", f'"{username}" "{template}" "{pubkey}"'])
    return redirect("/")
