from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.models.user import UserCreate
from app.services.auth_service import auth_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not auth_service.get_user("admin"):
        auth_service.create_user(UserCreate(
            username="admin",
            email="admin@mail.ru",
            password="qw123",
            full_name="Admin User"
        ))
        admin = auth_service.get_user("admin")
        admin.is_superuser = True
    yield

app = FastAPI(
    title="Groovy Music API",
    description="""🚀 Полнофункциональное API для музыкального сервиса с:
    \n- Аутентификацией JWT
    \n- Управлением треками, альбомами, плейлистами
    \n- Лайками и избранным
    \n- Поиском музыки""",
    version="1.0.0",
    contact={
        "name": "Mikhail Nikolaev",
        "email": "nmichail154@mail.ru",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
        "filter": True,
        "tagsSorter": "alpha",
        "operationsSorter": "method",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = Path(__file__).parent
static_dir = base_dir / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

from app.api.v1.endpoints import (
    auth as auth_router,
    tracks as tracks_router,
    playlist as playlists_router,
    album as albums_router,
    likes as likes_router
)

app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(tracks_router.router, prefix="/api/v1")
app.include_router(playlists_router.router, prefix="/api/v1")
app.include_router(albums_router.router, prefix="/api/v1")
app.include_router(likes_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)