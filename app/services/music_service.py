from typing import List, Optional
from ..models.track import Track
import os
from fastapi import HTTPException, status


class MusicService:
    def __init__(self):
        self.music_library = [
            Track(
                id=1,
                title="Bohemian Rhapsody",
                artist="Queen",
                duration=354,
                file_url="/static/music/bohemian_rhapsody.mp3",
                genre="Rock",
                album="A Night at the Opera",
                cover_url="/static/covers/queen_night.jpg"
            ),
        ]

    def get_all_tracks(self) -> List[Track]:
        return self.music_library

    def get_track_by_id(self, track_id: int) -> Track:
        for track in self.music_library:
            if track.id == track_id:
                return track
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )

    def search_tracks(self, query: str) -> List[Track]:
        return [track for track in self.music_library
                if query.lower() in track.title.lower()
                or query.lower() in track.artist.lower()]

    def get_audio_file(self, track_id: int):
        track = self.get_track_by_id(track_id)
        file_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "..",
            track.file_url.lstrip("/")
        ))

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audio file not found"
            )
        return file_path


music_service = MusicService()