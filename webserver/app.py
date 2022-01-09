import logging
from pathlib import Path

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)


def index(request):
    """
    Serves *index.html* of the frontend from `static/webapp/index.html`.
    If frontend hasn't been built, return a simple HTML page with instructions
    """
    index_file = Path("static/webapp/index.html")
    if not index_file.exists():
        index_file = "static/index.placeholder.html"
    with open(index_file) as f:
        content = f.read()
    return HTMLResponse(content)


app = Starlette(debug=True, routes=[
    Route("/", index)
])

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
