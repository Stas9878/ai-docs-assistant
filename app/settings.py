from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION_NAME: str
    EMBEDDING_MODEL_NAME: str
    VECTOR_SIZE: int

    OLLAMA_HOST: str
    OLLAMA_PORT: int
    OLLAMA_MODEL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def ollama_url(self):
        return f'http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}'



settings = Settings()