from typing import Dict, Set
from fastapi import HTTPException, status

class LikeService:
    def __init__(self):
        self.likes: Dict[int, Set[int]] = {}  # {user_id: set(track_ids)}

    def like_track(self, user_id: int, track_id: int) -> None:
        if user_id not in self.likes:
            self.likes[user_id] = set()
        self.likes[user_id].add(track_id)

    def unlike_track(self, user_id: int, track_id: int) -> None:
        if user_id in self.likes and track_id in self.likes[user_id]:
            self.likes[user_id].remove(track_id)

    def get_user_likes(self, user_id: int) -> Set[int]:
        return self.likes.get(user_id, set())

    def is_liked(self, user_id: int, track_id: int) -> bool:
        return user_id in self.likes and track_id in self.likes[user_id]

like_service = LikeService()