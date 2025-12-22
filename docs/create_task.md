### POST /api/v1/tasks
**Описание**: Создаёт новую задачу для пользователя.
**Параметры**: `title` (строка), `description` (строка)
**Ответ**:
```json
{"id": 42, "title": "string", "status": "pending"}