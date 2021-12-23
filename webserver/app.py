import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from authentication import views as auth_app
from account import views as account_app
from legacy import views as legacy_app
from gitserver import views as gitserver_app

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)


app = FastAPI(
    title="Waboorrt Web API Spec",
    version="0.1.0",
    openapi_tags=[
        {"name": "Authentication", "description": "Perform authentication."},
        {"name": "Account", "description": "Manage own user account. Requires authentication."},
        {"name": "Internal", "description": "API for internal services to fetch user information"},
        {"name": "legacy"},
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


app.include_router(legacy_app.router)
app.include_router(auth_app.router)
app.include_router(account_app.router)
app.include_router(gitserver_app.router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
