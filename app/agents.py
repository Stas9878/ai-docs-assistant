from crewai import Crew, Agent, LLM, Task

from app.logger import logger
from app.settings import settings

# Инициализация LLM (ваша дообученная модель)
llm = LLM(
    settings.OLLAMA_MODEL,
    base_url=f'http://{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}',
    temperature=0.0,
    timeout=60.0,
    max_tokens=400
)


def generate_documentation(query: str) -> str:
    """Генерирует документацию в строгом формате с помощью CrewAI."""
    logger.info(f'Запуск генерации по запросу: {query}')

    agent = Agent(
        role='API-документатор',
        goal='Генерировать документацию в строго заданном формате.',
        backstory=(
            'Ты специалист по API. Генерируй документацию ТОЛЬКО в формате:\n'
            '### МЕТОД /путь\n'
            '**Описание**: ... \n'
            '**Параметры**: ... \n'
            '**Ответ**:\n'
            '```json\n{...}\n```'
        ),
        llm=llm,
        verbose=False  # можно включить True для отладки
    )

    task = Task(
        description=f'Создай документацию для: {query}',
        expected_output='Документ в указанном формате. Ничего больше.',
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return str(result).strip()