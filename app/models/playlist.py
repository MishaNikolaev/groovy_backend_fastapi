from pydantic import BaseModel
from typing import List, Optional

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Playlist(PlaylistBase):
    id: int
    owner_id: int
    tracks: List[int] = []

    class Config:
        from_attributes = True