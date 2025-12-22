import logging
from pathlib import Path


# Создаём папку для логов, если её нет
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Форматтер
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Основной логгер
logger = logging.getLogger('ai-docs-assistant')
logger.setLevel(logging.INFO)

# 1. Обработчик для файла (все логи)
app_handler = logging.FileHandler(log_dir / 'app.log', encoding='utf-8')
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# 2. Обработчик для ошибок (только ошибки)
error_handler = logging.FileHandler(log_dir / 'errors.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# 3. Обработчик для консоли (все логи)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавляем все обработчики
logger.addHandler(app_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)