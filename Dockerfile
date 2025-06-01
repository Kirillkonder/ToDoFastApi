FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Скрипт запуска
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
