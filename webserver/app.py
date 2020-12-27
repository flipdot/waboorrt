import json
import logging
import os
import random
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect
import redis

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__, static_folder="static", template_folder="templates")
db = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)


@app.route("/")
def index():
    game_keys = sorted(db.keys("games:*"))
    games = [json.loads(db.get(k)) for k in game_keys]
    # games = [
    #     {"title": "A vs B", "timestamp": datetime.now(), "id": 420},
    #     {"title": "C vs B", "timestamp": datetime.now() - timedelta(minutes=3), "id": 520},
    #     {"title": "C vs A", "timestamp": datetime.now() - timedelta(minutes=6), "id": 620},
    # ]
    return render_template("index.html", games=games)


@app.route("/login", methods=["POST"])
def login():
    user_id = random.randint(0, 10000)  # probably we get some kind of unique stuff from oauth flow
    db.set(f"users:{user_id}", json.dumps({"botname": request.form.get("username")}))
    return redirect("/")
