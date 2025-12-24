import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.rag import initialize_rag_from_docs


@pytest.fixture(scope="session", autouse=True)
def initialize_rag_for_tests():
    """Инициализация RAG перед запуском всех тестов."""
    initialize_rag_from_docs()


@pytest.fixture
def client():
    return TestClient(app)


def test_search_existing(client):
    """Тест: поиск существующего документа."""
    response = client.post('/search', json={'query': 'Эндпоинт для получения профиля пользователя'})
    assert response.status_code == 200
    data = response.json()
    assert data['found'] is True
    assert 'GET /api/v1/profile' in data['content']


def test_search_not_found(client):
    """Тест: поиск несуществующего документа."""
    response = client.post('/search', json={'query': 'Что такое RAG?'})
    assert response.status_code == 200
    data = response.json()
    assert data['found'] is False
    assert 'Документация не найдена' in data['message']


def test_generate_new(client):
    """Тест: генерация нового документа (без записи на диск)."""
    query = 'Поиск по ключевым словам'

    # Убеждаемся, что документа нет
    search_resp = client.post('/search', json={'query': query})
    assert search_resp.json()['found'] is False

    # Мокаем save_document — не сохраняем файл, но возвращаем fake-путь
    with patch('app.main.save_document') as mock_save:
        mock_save.return_value = 'docs/test_search.md'

        # Генерация
        gen_resp = client.post('/generate', json={'query': query})
        assert gen_resp.status_code == 200
        data = gen_resp.json()
        assert data['success'] is True
        assert data['file_path'] == 'docs/test_search.md'
        mock_save.assert_called_once()


def test_health_check(client):
    """Тест: health-check возвращает статус."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'checks' in data