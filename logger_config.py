import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    # Создаем директорию для логов если её нет
    os.makedirs('logs', exist_ok=True)

    # Настраиваем основной логгер
    logger = logging.getLogger('gunicorn.error')
    logger.setLevel(logging.INFO)

    # Настраиваем форматирование
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Хендлер для файла с ротацией (10 файлов по 10MB)
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Хендлер для доступа
    access_handler = RotatingFileHandler(
        'logs/access.log',
        maxBytes=10*1024*1024,
        backupCount=10,
        encoding='utf-8'
    )
    access_handler.setFormatter(formatter)
    logging.getLogger('gunicorn.access').addHandler(access_handler)

    return logger