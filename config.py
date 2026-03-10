import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"

    chroma_persist_dir: str = "./data/chroma_db"
    sqlite_db_path: str = "./data/legallens.db"

    max_upload_size_mb: int = 50
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
