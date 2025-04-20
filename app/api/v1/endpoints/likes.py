from fastapi import APIRouter, Depends
from app.services.like_service import like_service
from typing import Set

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/tracks/{track_id}")
async def like_track(track_id: int, user_id: int = 1):
    like_service.like_track(user_id, track_id)
    return {"message": "Track liked"}

@router.delete("/tracks/{track_id}")
async def unlike_track(track_id: int, user_id: int = 1):
    like_service.unlike_track(user_id, track_id)
    return {"message": "Track unliked"}

@router.get("/", response_model=Set[int])
async def get_user_likes(user_id: int = 1):
    return like_service.get_user_likes(user_id)

@router.get("/tracks/{track_id}/is-liked", response_model=bool)
async def is_track_liked(track_id: int, user_id: int = 1):
    return like_service.is_liked(user_id, track_id)