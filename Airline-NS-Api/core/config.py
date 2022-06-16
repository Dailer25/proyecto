from pydantic import BaseSettings 
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_USERNAME: str = 'marianellab'
    DATABASE_PASSWORD: str = '123456'
    DATABASE_HOST: str = 'localhost'
    DATABASE_NAME: str = 'db-airline'
    DATABASE_URI: Optional[str] = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

    class Config:
        case_sensitive: bool = True
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()