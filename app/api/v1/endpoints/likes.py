from fastapi import APIRouter, Depends, HTTPException, status
from app.services.like_service import like_service
from typing import Set
from app.services.auth_service import auth_service
from app.models.user import UserInDB
from typing import Annotated

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/tracks/{track_id}")
async def like_track(
    track_id: int,
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    like_service.like_track(str(current_user.id), track_id)
    return {"message": "Track liked"}

@router.delete("/tracks/{track_id}")
async def unlike_track(
    track_id: int,
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    like_service.unlike_track(str(current_user.id), track_id)
    return {"message": "Track unliked"}

@router.get("/", response_model=Set[int])
async def get_user_likes(
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    return like_service.get_user_likes(str(current_user.id))

@router.get("/tracks/{track_id}/is-liked", response_model=bool)
async def is_track_liked(
    track_id: int,
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    return like_service.is_liked(str(current_user.id), track_id)