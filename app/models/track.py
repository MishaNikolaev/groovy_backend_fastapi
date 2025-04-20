from pydantic import BaseModel
from typing import Optional

class Track(BaseModel):
    id: int
    title: str
    artist: str
    duration: int
    file_url: str
    genre: Optional[str] = None
    album: Optional[str] = None
    cover_url: Optional[str] = None