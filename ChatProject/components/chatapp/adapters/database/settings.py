from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'sqlite:///C:\\temp\\simple_chat.db'
