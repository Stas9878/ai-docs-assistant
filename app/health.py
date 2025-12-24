import httpx

from app.logger import logger
from app.settings import settings
from app.rag import search_documentation


async def check_qdrant():
    """Проверяет доступность Qdrant через REST API."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f'{settings.qdrant_url}/collections')
            return resp.status_code == 200
    except Exception as e:
        logger.error(f'Qdrant недоступен: {e}')
        return False


async def check_ollama():
    """Проверяет доступность Ollama."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f'{settings.ollama_url}/api/tags')
            return resp.status_code == 200
    except Exception as e:
        logger.error(f'Ollama недоступен: {e}')
        return False


def check_docs():
    """Проверяет, есть ли документы в docs/."""
    from pathlib import Path
    return len(list(Path('docs').glob('*.md'))) > 0


def run_rag_canary_check() -> bool:
    """
    Выполняет канареечный запрос к RAG.
    Возвращает True, если система отвечает ожидаемо.
    """
    query = "Эндпоинт для получения профиля"
    result = search_documentation(query, similarity_threshold=0.6)
    if not result:
        return False
    return "GET /api/v1/profile" in result


async def check_all_services() -> dict:
    """Возвращает полный отчёт о состоянии сервиса."""
    qdrant = await check_qdrant()
    ollama = await check_ollama()
    docs = check_docs()
    rag_canary = run_rag_canary_check()

    status = 'healthy' if all([qdrant, ollama, docs, rag_canary]) else 'unhealthy'

    return {
        'status': status,
        'checks': {
            'qdrant': qdrant,
            'ollama': ollama,
            'docs': docs,
            'rag_canary': rag_canary
        }
    }