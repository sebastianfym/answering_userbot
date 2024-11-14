import os
import sys
from typing import ClassVar, List

from dotenv import load_dotenv
from pyrogram import Client
from pydantic_settings import BaseSettings
from loguru import logger
load_dotenv()


class Settings(BaseSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SYS_PATH:
            self.SYS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
        sys.path.append(self.SYS_PATH)

        logger.add(
            self.LOG_FILE,
            format=self.LOG_FORMAT,
            level=self.LOG_LEVEL,
            rotation=self.LOG_ROTATION,
            compression=self.LOG_COMPRESSION,
            serialize=self.LOG_SERIALIZE
        )

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    API_ID: str
    API_HASH: str

    BOT_TOKEN: str

    SYS_PATH: str = ""

    stop_words: List = ["прекрасно", "ожидать"]

    LOG_FILE: str = "answering_bot.log"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    LOG_LEVEL: str = "DEBUG"
    LOG_ROTATION: str = "10 MB"
    LOG_COMPRESSION: str = "zip"
    LOG_SERIALIZE: bool = True

    logger: ClassVar = logger

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
client = Client(
    "my_bot",
    api_id=settings.API_ID, api_hash=settings.API_HASH
)
