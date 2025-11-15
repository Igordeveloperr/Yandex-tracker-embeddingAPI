# Yandex Tracker Embedding API

API для генерации эмбеддингов на основе модели ai-forever/ru-en-RoSBERTa

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
python main.py
```

## API Методы

### GET /

Проверка состояния API

**Пример запроса:**
```bash
curl http://127.0.0.1:8000/
```

**Пример ответа:**
```json
{
  "message": "Yandex Tracker Embedding API",
  "status": "running"
}
```

### POST /embeddings

Генерирует эмбеддинг для переданной строки

**Тело запроса:**
```json
{
  "text": "строка, для которой нужно сгенерировать эмбеддинг"
}
```

**Пример запроса:**
```bash
curl -X POST http://127.0.0.1:8000/embeddings \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, мир!"}'
```

**Пример ответа:**
```json
{
  "embedding": [0.1, 0.2, 0.3, ...]
}
```

## Конфигурация

Конфигурация находится в файле `config.py`:
- `MODEL_NAME` - название модели для генерации эмбеддингов
- `MAX_LENGTH` - максимальная длина текста
- `DEVICE` - устройство для вычислений (CPU или GPU)
- `BATCH_SIZE` - размер батча