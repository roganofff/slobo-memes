from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title='slobo-memes', docs_url='/swagger')
    return app