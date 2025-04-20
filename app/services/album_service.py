from typing import List, Optional
from ..models.album import Album, AlbumCreate, AlbumUpdate
from fastapi import HTTPException, status

class AlbumService:
    def __init__(self):
        self.albums = []
        self.current_id = 0

    def create_album(self, album: AlbumCreate) -> Album:
        self.current_id += 1
        new_album = Album(
            id=self.current_id,
            **album.model_dump()
        )
        self.albums.append(new_album)
        return new_album

    def get_album(self, album_id: int) -> Album:
        for album in self.albums:
            if album.id == album_id:
                return album
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    def update_album(self, album_id: int, album_update: AlbumUpdate) -> Album:
        for i, album in enumerate(self.albums):
            if album.id == album_id:
                update_data = album_update.model_dump(exclude_unset=True)
                updated_album = album.model_copy(update=update_data)
                self.albums[i] = updated_album
                return updated_album
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    def delete_album(self, album_id: int) -> None:
        self.albums = [a for a in self.albums if a.id != album_id]

    def add_track_to_album(self, album_id: int, track_id: int) -> Album:
        album = self.get_album(album_id)
        if track_id not in album.tracks:
            album.tracks.append(track_id)
        return album

    def remove_track_from_album(self, album_id: int, track_id: int) -> Album:
        album = self.get_album(album_id)
        album.tracks = [t for t in album.tracks if t != track_id]
        return album

album_service = AlbumService()