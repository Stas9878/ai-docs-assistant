from pathlib import Path
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from app.settings import settings

# Подключение к Qdrant
client = QdrantClient(settings.QDRANT_HOST, port=settings.QDRANT_PORT)
collection_name = 'api_docs'

# Инициализация эмбеддингов
embeddings = OllamaEmbeddings(model='nomic-embed-text')

# Создаём коллекцию при первом запуске
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config={'size': 768, 'distance': 'Cosine'}
    )

# LangChain-совместимое векторное хранилище
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings
)


def initialize_rag_from_docs():
    """Загружает все .md-файлы из docs/ в векторную БД при старте."""
    docs = []
    for file in Path('docs').glob('*.md'):
        with open(file, 'r') as f:
            content = f.read()
            docs.append(Document(page_content=content, metadata={'source': str(file)}))

    if docs:
        vector_store.add_documents(docs)
        print(f'Загружено {len(docs)} документов в RAG при инициализации.')