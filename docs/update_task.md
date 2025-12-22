### PATCH /api/v1/tasks/{id}
**Описание**: Обновляет статус задачи.
**Параметры**: `id` (путь), `status` (строка: "pending", "completed")
**Ответ**:
```json
{"id": 42, "status": "completed"}