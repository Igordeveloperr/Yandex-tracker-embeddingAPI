# Используем базовый образ Python с PyTorch (CPU версия)
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . /app

# Открываем порт, который будет использоваться для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]