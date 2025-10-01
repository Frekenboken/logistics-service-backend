from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # DB_URL: str
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_HOST: str
    # DB_PORT: int
    # DB_NAME: str
    # DB_ECHO: bool
    #
    # BOT_TOKEN: str
    # ADMIN_CHAT_ID: int
    # ADMIN_TOPIC_THREAD_ID: int
    # USER_TOPIC_THREAD_ID: int


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()