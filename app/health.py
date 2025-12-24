import httpx

from app.logger import logger
from app.settings import settings


async def check_qdrant():
    """Проверяет доступность Qdrant через REST API."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f'http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}/collections')
            return resp.status_code == 200
    except Exception as e:
        logger.error(f'Qdrant недоступен: {e}')
        return False


async def check_ollama():
    """Проверяет доступность Ollama."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f'http://{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}/api/tags')
            return resp.status_code == 200
    except Exception as e:
        logger.error(f'Ollama недоступен: {e}')
        return False


def check_docs():
    """Проверяет, есть ли документы в docs/."""
    from pathlib import Path
    return len(list(Path('docs').glob('*.md'))) > 0