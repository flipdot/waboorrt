import logging
from datetime import datetime, timedelta

from flask import Flask, render_template
import redis

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__, static_folder="static", template_folder="templates")
db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


@app.route("/")
def index():
    game_keys = sorted(db.keys("games:*"))
    games = [db.get(k) for k in game_keys]
    # games = [
    #     {"title": "A vs B", "timestamp": datetime.now(), "id": 420},
    #     {"title": "C vs B", "timestamp": datetime.now() - timedelta(minutes=3), "id": 520},
    #     {"title": "C vs A", "timestamp": datetime.now() - timedelta(minutes=6), "id": 620},
    # ]
    return render_template("index.html", games=games)
