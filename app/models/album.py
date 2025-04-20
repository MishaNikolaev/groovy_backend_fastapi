from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AlbumBase(BaseModel):
    title: str
    artist_id: int
    release_date: Optional[datetime] = None
    cover_url: Optional[str] = None

class AlbumCreate(AlbumBase):
    pass

class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[int] = None
    release_date: Optional[datetime] = None
    cover_url: Optional[str] = None

class Album(AlbumBase):
    id: int
    tracks: List[int] = []
    tracks_count: int = 0
    duration: int = 0

    class Config:
        from_attributes = True
