from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from app.api.v1.endpoints import (
    tracks as tracks_router,
    playlist as playlists_router,
    album as albums_router,
    likes as likes_router
)

app = FastAPI(
    title="Music API",
    description="Groovy API with playlists, albums and likes",
    version="1.0.0"
)

base_dir = Path(__file__).parent
static_dir = base_dir / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(tracks_router.router)
app.include_router(playlists_router.router)
app.include_router(albums_router.router)
app.include_router(likes_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)