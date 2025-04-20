import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Music API", description="API для мобильного приложения")


class Track(BaseModel):
    id: int
    title: str
    artist: str
    duration: int
    file_url: str

mock_music_library = [
    Track(id=1, title="Bohemian Rhapsody", artist="Queen", duration=354, file_url="https://example.com/music/1.mp3"),
    Track(id=2, title="Imagine", artist="John Lennon", duration=183, file_url="https://example.com/music/2.mp3"),
    Track(id=3, title="Billie Jean", artist="Michael Jackson", duration=294, file_url="https://example.com/music/3.mp3"),
]

@app.get("/tracks/", response_model=List[Track], summary="Получить список всех треков")
async def get_all_tracks():
    return mock_music_library

@app.get("/tracks/{track_id}", response_model=Track, summary="Получить трек по ID")
async def get_track(track_id: int):
    for track in mock_music_library:
        if track.id == track_id:
            return track
    return {"error": "Track not found"}, 404
