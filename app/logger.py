import logging
from pathlib import Path


# Создаём папку для логов, если её нет
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Создаём форматтер
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Логгер приложения
logger = logging.getLogger('ai-docs-assistant')
logger.setLevel(logging.INFO)

# Обработчик для всех логов (INFO и выше)
app_handler = logging.FileHandler(log_dir / 'app.log', encoding='utf-8')
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# Обработчик только для ошибок (ERROR и выше)
error_handler = logging.FileHandler(log_dir / 'errors.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(app_handler)
logger.addHandler(error_handler)

# Запрещаем распространение логов выше (чтобы избежать дублирования в консоли)
logger.propagate = False