from fastapi import APIRouter, Query, Depends
from fastapi.responses import FileResponse
from typing import List, Optional, Annotated

from app.services.music_service import music_service
from app.models.track import Track, TrackCreate, TrackUpdate
from app.models.user import UserInDB
from app.services.auth_service import auth_service

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", response_model=List[Track], summary="Get all tracks")
async def get_tracks(
    skip: int = 0,
    limit: int = 10,
    genre: Optional[str] = None,
    artist_id: Optional[int] = None
):
    return music_service.get_tracks(skip, limit, genre, artist_id)

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
    query: str = Query(..., min_length=2)
):
    return music_service.search_tracks(query)

@router.get("/stats/top-tracks", response_model=List[Track], summary="Top tracks by plays")
async def get_top_tracks(limit: int = 10):
    return sorted(
        music_service.get_all_tracks(),
        key=lambda x: x.plays_count,
        reverse=True
    )[:limit]

@router.post("/{track_id}/play", summary="Record play for a track")
async def record_play(
    track_id: int,
        current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    music_service.record_play(track_id, current_user.id)
    return {"status": "recorded"}

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
