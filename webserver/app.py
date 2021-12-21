import json
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from constants import VALID_REPO_TEMPLATES
from database import redis_db
from routers import auth, account

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)


app = FastAPI(
    title="Waboorrt Web API Spec",
    version="0.1.0",
    openapi_tags=[
        {"name": "default"},
        {"name": "Authentication", "description": "Perform authentication."},
        {"name": "Account", "description": "Manage own user account. Requires authentication."},
        {"name": "Non-API", "description": "Provided for convenience. Can be replaced by a stupid webserver."},
    ]
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Non-API"], response_class=HTMLResponse)
def index():
    """
    Serves *index.html* of the frontend from `static/webapp/index.html`.
    If frontend hasn't been built, return a simple HTML page with instructions
    """
    index_file = Path("static/webapp/index.html")
    if not index_file.exists():
        index_file = "static/index.placeholder.html"
    with open(index_file) as f:
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
        from_game_str = redis_db.get(from_key)
        if not from_game_str:
            raise HTTPException(status_code=404, detail="game not found")
        from_game = json.loads(from_game_str)
        max_range = float(from_game.get("timestamp"))
    else:
        max_range = "+inf"
    game_keys = [
        f"game:{x}:summary" for x in
        redis_db.zrevrangebyscore("matches_by_time", max_range, "-inf", start=0, num=num)
    ]
    games = [json.loads(redis_db.get(k)) for k in game_keys]
    return games


@app.get("/api/games/{game_id}")
def game_detail(game_id: str):
    """
    Returns the logfile of the requested game. `game_id` can be fetched from `/api/games`.
    """
    history = redis_db.get(f"game:{game_id}:history")
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


app.include_router(auth.router)
app.include_router(account.router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
