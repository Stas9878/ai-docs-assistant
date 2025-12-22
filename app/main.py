import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from app.logger import logger
from app.rag import initialize_rag_from_docs


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Инициализация RAG из docs/')

    # Выполняем загрузку эмбеддингов в отдельном потоке
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, initialize_rag_from_docs)

    logger.info('Сервис готов к работе')
    yield


app = FastAPI(title='AI Docs Assistant', lifespan=lifespan)


@app.get('/health')
def health_check():
    return {'status': 'ok'}