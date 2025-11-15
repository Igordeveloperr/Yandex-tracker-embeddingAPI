import torch

# Конфигурационный файл для API
MODEL_NAME = "ai-forever/ru-en-RoSBERTa"
MAX_LENGTH = 512
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 16