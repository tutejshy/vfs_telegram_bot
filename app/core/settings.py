from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    TOKEN: str
    CHAT_ID: str
    DEV_CHAT_ID: str

    BOT_LOGIN: str
    BOT_PASSWORD: str

    DATABASE_URI: str

    LOGINS_ENCODED: Optional[str]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
