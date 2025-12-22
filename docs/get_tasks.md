### GET /api/v1/tasks
**Описание**: Возвращает список задач текущего пользователя.
**Параметры**: `status` (необязательный, строка: "pending", "completed")
**Ответ**:
```json
[{"id": 42, "title": "string", "status": "pending"}]
```