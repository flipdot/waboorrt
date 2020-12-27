from datetime import datetime, timedelta

from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    games = [
        {"title": "A vs B", "timestamp": datetime.now(), "id": 420},
        {"title": "C vs B", "timestamp": datetime.now() - timedelta(minutes=3), "id": 520},
        {"title": "C vs A", "timestamp": datetime.now() - timedelta(minutes=6), "id": 620},
    ]
    return render_template("index.html", games=games)
