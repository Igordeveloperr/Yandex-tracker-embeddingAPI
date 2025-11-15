from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
import logging
from config import MODEL_NAME, MAX_LENGTH, DEVICE

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Yandex Tracker Embedding API",
              description="API для генерации эмбеддингов на основе модели ai-forever/ru-en-RoSBERTa",
              version="1.0.0")

class SingleEmbeddingRequest(BaseModel):
    text: str

# Загрузка модели и токенизатора
logger.info(f"Загрузка модели {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
device = torch.device(DEVICE if torch.cuda.is_available() else "cpu")
model.to(device)
logger.info(f"Модель загружена на {device}")

def mean_pooling(model_output, attention_mask):
    """
    Применение mean pooling к output модели для получения эмбеддингов
    """
    token_embeddings = model_output[0]  # Последний скрытый слой
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

@app.post("/embeddings", description="Принимает строку и возвращает её эмбеддинг")
async def get_embedding(request: SingleEmbeddingRequest):
    """
    Генерирует эмбеддинг для переданной строки
    """
    try:
        # Токенизация текста
        encoded_input = tokenizer(request.text,
                                  padding=True,
                                  truncation=True,
                                  max_length=MAX_LENGTH,
                                  return_tensors='pt')

        # Переносим тензоры на устройство
        encoded_input = {key: val.to(device) for key, val in encoded_input.items()}

        # Получаем эмбеддинги
        with torch.no_grad():
            model_output = model(**encoded_input)
            embedding = mean_pooling(model_output, encoded_input['attention_mask'])
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

        # Конвертируем в список для JSON сериализации
        embedding_list = embedding.cpu().numpy().flatten().tolist()

        return {"embedding": embedding_list}
    except Exception as e:
        logger.error(f"Ошибка при генерации эмбеддинга: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации эмбеддинга: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Yandex Tracker Embedding API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)