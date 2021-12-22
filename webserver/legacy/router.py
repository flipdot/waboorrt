import json

from fastapi import APIRouter, HTTPException

from constants import VALID_REPO_TEMPLATES
from database import redis_db

router = APIRouter(
    prefix="/api",
    tags=["legacy"],
)


@router.get("/api/games")
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


@router.get("/api/games/{game_id}")
def game_detail(game_id: str):
    """
    Returns the logfile of the requested game. `game_id` can be fetched from `/api/games`.
    """
    history = redis_db.get(f"game:{game_id}:history")
    if not history:
        raise HTTPException(status_code=404)

    return json.loads(history)


@router.get("/api/templates")
def valid_repo_templates():
    """
    List of available repository templates. Used by the frontend to offer the user a list of programming
    languages to choose from. Their choice initiates a new repository which contains files from the
    corresponding template directory.
    """
    return VALID_REPO_TEMPLATES
