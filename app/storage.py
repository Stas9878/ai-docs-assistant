import re
from pathlib import Path

from app.logger import logger

DOCS_DIR = Path('docs')
DOCS_DIR.mkdir(exist_ok=True)

# Словари для сопоставления подстрок → терминам
ACTION_KEYWORDS = {
    'get': ['получ', 'прочит', 'профиль', 'profile', 'данные о', 'информация о', 'посмотреть'],
    'create': ['созда', 'добав', 'новая', 'новый', 'сделать'],
    'delete': ['удали', 'удал', 'удаление', 'уничтож', 'remove'],
    'update': ['обнов', 'измени', 'измен', 'статус', 'редактируй', 'edit']
}

ENTITY_KEYWORDS = {
    'user': ['пользовател', 'user', 'юзер', 'аккаунт'],
    'task': ['задач', 'task', 'дело', 'todo'],
    'profile': ['профил', 'profile', 'личн', 'инфо о себе']
}


def _slugify(text: str) -> str:
    """
    Преобразует запрос в имя файла вида action_entity.
    """
    text = text.lower()

    # Определяем действие
    action = 'api'
    for act, keywords in ACTION_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            action = act
            break  # используем первое найденное (можно менять логику приоритета)

    # Определяем сущность
    entity = None
    for ent, keywords in ENTITY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            entity = ent
            break

    # Формируем название
    if entity:
        return f"{action}_{entity}"
    return action


def save_document(content: str, query: str) -> str:
    base_name = _slugify(query)
    # Очищаем от случайных символов
    base_name = re.sub(r'[^a-z0-9_]', '', base_name)
    if not base_name:
        base_name = 'api_doc'

    file_path = DOCS_DIR / f'{base_name}.md'
    counter = 1
    while file_path.exists():
        file_path = DOCS_DIR / f'{base_name}_{counter}.md'
        counter += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())

    logger.info(f'Документ сохранён: {file_path}')
    return str(file_path)