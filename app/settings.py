from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_HOST: str
    QDRANT_PORT: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()