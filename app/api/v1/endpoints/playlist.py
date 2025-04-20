from fastapi import APIRouter, Depends, HTTPException, status
from app.services.playlist_service import playlist_service
from app.models.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from typing import List

router = APIRouter(prefix="/playlists", tags=["playlists"])

@router.post("/", response_model=Playlist, status_code=201)
async def create_playlist(playlist: PlaylistCreate, owner_id: int = 1):  
    return playlist_service.create_playlist(playlist, owner_id)

@router.get("/{playlist_id}", response_model=Playlist)
async def get_playlist(playlist_id: int):
    return playlist_service.get_playlist(playlist_id)

@router.patch("/{playlist_id}", response_model=Playlist)
async def update_playlist(playlist_id: int, playlist_update: PlaylistUpdate):
    return playlist_service.update_playlist(playlist_id, playlist_update)

@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(playlist_id: int):
    playlist_service.delete_playlist(playlist_id)

@router.post("/{playlist_id}/tracks/{track_id}", response_model=Playlist)
async def add_track_to_playlist(playlist_id: int, track_id: int):
    return playlist_service.add_track_to_playlist(playlist_id, track_id)

@router.delete("/{playlist_id}/tracks/{track_id}", response_model=Playlist)
async def remove_track_from_playlist(playlist_id: int, track_id: int):
    return playlist_service.remove_track_from_playlist(playlist_id, track_id)