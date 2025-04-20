from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings:
    AUDIO_DIR = BASE_DIR / "static" / "music"
    COVERS_DIR = BASE_DIR / "static" / "covers"
    PLAYLIST_COVERS_DIR = BASE_DIR / "static" / "playlist_covers"

    ALLOWED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg"]
    ALLOWED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]

    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


settings = Settings()