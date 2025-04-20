from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from app.api.v1.endpoints.tracks import router as tracks_router

app = FastAPI(
    title="Music API",
    description="Groovy API",
    version="1.0.0"
)

base_dir = Path(__file__).parent
static_dir = base_dir / "static"

static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(tracks_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)