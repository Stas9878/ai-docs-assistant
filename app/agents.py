from crewai import Agent, Task, Crew, LLM

from app.logger import logger
from app.settings import settings

# Инициализация LLM (общая для всех агентов)
llm = LLM(
    model=settings.OLLAMA_MODEL,
    base_url=f'http://{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}',
    temperature=0.0,
    timeout=60.0,
    max_tokens=300
)


def _create_generator_agent():
    return Agent(
        role='API-документатор',
        goal='Генерировать документацию в строгом формате.',
        backstory=(
            'Ты специалист по API. Генерируй документацию ТОЛЬКО в формате:\n'
            '### МЕТОД /путь\n'
            '**Описание**: ... \n'
            '**Параметры**: ... \n'
            '**Ответ**:\n'
            '```json\n{...}\n```'
        ),
        llm=llm,
        verbose=False
    )


def _create_validator_agent():
    return Agent(
        role='Валидатор документации',
        goal='Проверять соответствие документа строгому формату.',
        backstory=(
            'Ты строгий QA-инженер. Ты должен проверить, что документ содержит:\n'
            '1. Строку вида "### МЕТОД /путь",\n'
            '2. Блок "**Описание**:",\n'
            '3. Блок "**Параметры" или "**Параметры пути**:",\n'
            '4. Блок "**Ответ**:" с JSON-примером в тройных кавычках.\n'
            'Если всё есть — ответь "valid". Иначе — "invalid".'
        ),
        llm=llm,
        verbose=False
    )


def generate_and_validate_documentation(query: str) -> str | None:
    """
    Генерирует документацию и проверяет её валидатором.
    Возвращает контент, только если он валиден.
    """
    logger.info(f'Запуск генерации по запросу: {query}')

    # === Этап 1: Генерация ===
    generator = _create_generator_agent()
    gen_task = Task(
        description=f'Создай документацию для: {query}',
        expected_output='Документ в строгом формате. Ничего больше.',
        agent=generator
    )
    gen_crew = Crew(agents=[generator], tasks=[gen_task])
    raw_content = str(gen_crew.kickoff()).strip()

    if not raw_content:
        logger.error(f'Генерация вернула пустой результат для запроса: {query}')
        return None

    # === Этап 2: Валидация ===
    validator = _create_validator_agent()
    val_task = Task(
        description=f'Проверь документ:\n\n{raw_content}',
        expected_output='Только "valid" или "invalid", без пояснений.',
        agent=validator
    )
    val_crew = Crew(agents=[validator], tasks=[val_task])
    validation_result = str(val_crew.kickoff()).strip().lower()

    if 'valid' in validation_result:
        logger.info('Документ прошёл валидацию для запроса: {query}')
        return raw_content
    else:
        logger.warning(f'Документ не прошёл валидацию: {validation_result} для запроса: {query}')
        return None