import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from app.logger import logger
from app.storage import save_document
from app.agents import generate_documentation
from app.rag import initialize_rag_from_docs, search_documentation
from app.schemas import SearchRequest, SearchResponse, GenerateRequest, GenerateResponse


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


@app.post('/search', response_model=SearchResponse)
def search_docs(request: SearchRequest):
    """
    Выполняет семантический поиск в базе документации.
    """
    result = search_documentation(request.query)

    if result:
        return SearchResponse(found=True, content=result)
    else:
        return SearchResponse(
            found=False,
            message='Документация не найдена. Используйте /generate для создания новой.'
        )


@app.post('/generate', response_model=GenerateResponse)
def generate_docs(request: GenerateRequest):
    """
    Генерирует новую документацию и сохраняет её в docs/.
    """
    # 1. Проверяем, не существует ли уже документ
    if search_documentation(request.query, similarity_threshold=0.7):
        return GenerateResponse(
            success=False,
            message='Документ уже существует. Используйте /search.'
        )

    try:
        # 2. Генерация через агента
        content = generate_documentation(request.query)

        # 3. Базовая валидация: должен содержать заголовок
        if not content.strip().startswith('### '):
            logger.error('Сгенерированный документ не соответствует формату')
            return GenerateResponse(
                success=False,
                message='Ошибка генерации: неверный формат документа.'
            )

        # 4. Сохранение
        file_path = save_document(content, request.query)

        # 5. Обновить RAG
        initialize_rag_from_docs()

        return GenerateResponse(
            success=True,
            message='Документ успешно создан и сохранён.',
            file_path=file_path
        )

    except Exception as e:
        logger.error(f'Ошибка генерации документа: {e}', exc_info=True)
        return GenerateResponse(
            success=False,
            message=f'Ошибка генерации: {str(e)}'
        )