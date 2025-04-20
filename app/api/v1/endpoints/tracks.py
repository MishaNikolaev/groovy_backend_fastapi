from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.services.music_service import music_service
from app.models.track import Track, TrackCreate, TrackUpdate
from typing import List

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", response_model=List[Track], summary="Get all tracks")
async def get_all_tracks():
    return music_service.get_all_tracks()

@router.get("/{track_id}", response_model=Track, summary="Get track by ID")
async def get_track(track_id: int):
    return music_service.get_track_by_id(track_id)

@router.get("/{track_id}/play", summary="Play track")
async def play_track(track_id: int):
    file_path = music_service.get_audio_file(track_id)
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=f"track_{track_id}.mp3"
    )

@router.get("/search/", response_model=List[Track], summary="Search tracks")
async def search_tracks(
    query: str = Query(..., min_length=2, description="Search query")
):
    return music_service.search_tracks(query)

@router.post("/", response_model=Track, status_code=201, summary="Create new track")
async def create_track(track: TrackCreate):
    return music_service.create_track(track)

@router.patch("/{track_id}", response_model=Track, summary="Update track")
async def update_track(track_id: int, track_update: TrackUpdate):
    return music_service.update_track(track_id, track_update)

@router.delete("/{track_id}", status_code=204, summary="Delete track")
async def delete_track(track_id: int):
    music_service.delete_track(track_id)
    return None