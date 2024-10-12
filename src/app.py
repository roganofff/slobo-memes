from fastapi import FastAPI

from src.api import router


def create_app() -> FastAPI:
    global app
    app = FastAPI(title='slobo-memes', docs_url='/swagger')
    app.include_router(router)
    return app
