from typing import List, Optional
from ..models.playlist import Playlist, PlaylistCreate, PlaylistUpdate
from fastapi import HTTPException, status

class PlaylistService:
    def __init__(self):
        self.playlists = []
        self.current_id = 0

    def create_playlist(self, playlist: PlaylistCreate, owner_id: int) -> Playlist:
        self.current_id += 1
        new_playlist = Playlist(
            id=self.current_id,
            owner_id=owner_id,
            **playlist.model_dump()
        )
        self.playlists.append(new_playlist)
        return new_playlist

    def get_playlist(self, playlist_id: int) -> Playlist:
        for playlist in self.playlists:
            if playlist.id == playlist_id:
                return playlist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )

    def update_playlist(self, playlist_id: int, playlist_update: PlaylistUpdate) -> Playlist:
        for i, playlist in enumerate(self.playlists):
            if playlist.id == playlist_id:
                update_data = playlist_update.model_dump(exclude_unset=True)
                updated_playlist = playlist.model_copy(update=update_data)
                self.playlists[i] = updated_playlist
                return updated_playlist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )

    def delete_playlist(self, playlist_id: int) -> None:
        self.playlists = [p for p in self.playlists if p.id != playlist_id]

    def add_track_to_playlist(self, playlist_id: int, track_id: int) -> Playlist:
        playlist = self.get_playlist(playlist_id)
        if track_id not in playlist.tracks:
            playlist.tracks.append(track_id)
        return playlist

    def remove_track_from_playlist(self, playlist_id: int, track_id: int) -> Playlist:
        playlist = self.get_playlist(playlist_id)
        playlist.tracks = [t for t in playlist.tracks if t != track_id]
        return playlist

playlist_service = PlaylistService()