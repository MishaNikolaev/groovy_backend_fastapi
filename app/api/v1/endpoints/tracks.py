from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.services.music_service import music_service
from app.models.track import Track
from typing import List

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", response_model=List[Track], summary="Получить список всех треков")
async def get_all_tracks():
    return music_service.get_all_tracks()

@router.get("/{track_id}", response_model=Track, summary="Получить трек по ID")
async def get_track(track_id: int):
    return music_service.get_track_by_id(track_id)

@router.get("/{track_id}/play", summary="Прослушать трек")
async def play_track(track_id: int):
    file_path = music_service.get_audio_file(track_id)
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=f"track_{track_id}.mp3"
    )

@router.get("/search/", response_model=List[Track], summary="Поиск треков")
async def search_tracks(
    query: str = Query(..., min_length=2, description="Поисковый запрос")
):
    return music_service.search_tracks(query)