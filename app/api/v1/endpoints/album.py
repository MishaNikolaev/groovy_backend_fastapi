from fastapi import APIRouter
from app.services.album_service import album_service
from app.models.album import Album, AlbumCreate, AlbumUpdate
from typing import List

router = APIRouter(prefix="/albums", tags=["albums"])

@router.post("/", response_model=Album, status_code=201)
async def create_album(album: AlbumCreate):
    return album_service.create_album(album)

@router.get("/", response_model=List[Album])
async def get_all_albums():
    return album_service.albums

@router.get("/{album_id}", response_model=Album)
async def get_album(album_id: int):
    return album_service.get_album(album_id)

@router.patch("/{album_id}", response_model=Album)
async def update_album(album_id: int, album_update: AlbumUpdate):
    return album_service.update_album(album_id, album_update)

@router.delete("/{album_id}", status_code=204)
async def delete_album(album_id: int):
    album_service.delete_album(album_id)

@router.post("/{album_id}/tracks/{track_id}", response_model=Album)
async def add_track_to_album(album_id: int, track_id: int):
    return album_service.add_track_to_album(album_id, track_id)

@router.delete("/{album_id}/tracks/{track_id}", response_model=Album)
async def remove_track_from_album(album_id: int, track_id: int):
    return album_service.remove_track_from_album(album_id, track_id)