from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    id: UUID
    username: str
    email: str
    is_admin: bool = False

class TrackBase(BaseModel):
    title: str
    artist_id: int
    duration: int
    file_url: str
    genre_id: Optional[int] = None
    album_id: Optional[int] = None
    cover_url: Optional[str] = None

class TrackCreate(TrackBase):
    pass

class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[int] = None
    duration: Optional[int] = None
    file_url: Optional[str] = None
    genre_id: Optional[int] = None
    album_id: Optional[int] = None
    cover_url: Optional[str] = None

class Track(TrackBase):
    id: int
    created_at: datetime
    plays_count: int = 0
    likes_count: int = 0

    class Config:
        from_attributes = True

class AlbumBase(BaseModel):
    title: str
    artist_id: int
    release_date: Optional[datetime] = None
    cover_url: Optional[str] = None

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    id: int
    tracks_count: int
    duration: int

class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    tracks_count: int
    albums_count: int

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    tracks_count: int

class PlaylistBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = False

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class Playlist(PlaylistBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    tracks_count: int
    duration: int
    tracks: List[Track] = []