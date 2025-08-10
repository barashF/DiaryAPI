from fastapi import FastAPI

from diary.router import router as diary_router
from config.database import init_db


def _init_routers(app: FastAPI):
    app.include_router(diary_router)


def create_app():
    app = FastAPI(title="Diary", docs_url="/api/swagger")

    @app.on_event("startup")
    async def startup_event():
        await init_db()

    _init_routers(app)
    return app
