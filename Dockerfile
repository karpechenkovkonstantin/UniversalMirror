FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем директорию для логов
RUN mkdir -p logs

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 3000

CMD ["gunicorn", "--timeout", "60", "--workers", "1", "--threads", "1", "--bind", "0.0.0.0:3000", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "app:app"]