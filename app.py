from flask import Flask, send_from_directory, abort, request
import yaml
import os
import requests
import schedule
import time
import threading
import configparser
from croniter import croniter
from datetime import datetime
from logger_config import setup_logger

app = Flask(__name__)
logger = setup_logger()

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Settings']

def download_file(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Файл {url} успешно загружен в {path}")
    except Exception as e:
        logger.error(f"Ошибка загрузки {url}: {str(e)}")

def sync_files():
    settings = load_config()
    logger.info("Начало синхронизации")
    
    try:
        with open('links.yaml', 'r') as f:
            links = yaml.safe_load(f)
            
        for main_dir, subdirs in links.items():
            for subdir, files in subdirs.items():
                for file_url in files:
                    file_name = file_url.split('/')[-1]
                    save_path = os.path.join('.', main_dir, subdir, file_name)
                    download_file(file_url, save_path)
        
        logger.info("Файлы успешно синхронизированны")
    except Exception as e:
        logger.error(f"Ошибка синхронизации: {str(e)}")

def schedule_sync():
    settings = load_config()
    cron_schedule = settings.get('sync_schedule', '0 0 * * *')
    
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    next_run = croniter(cron_schedule, datetime.now()).get_next(datetime)
    schedule.every().day.at(next_run.strftime("%H:%M")).do(sync_files)
    
    logger.info(f"Синхронизация по CRON: {cron_schedule}")
    
    thread = threading.Thread(target=run_schedule)
    thread.daemon = True
    thread.start()

@app.route('/links/<path:filepath>')
def serve_file(filepath):
    client_ip = request.remote_addr
    logger.info(f"{client_ip} запросил: {filepath}")
    
    try:
        with open('links.yaml', 'r') as f:
            links = yaml.safe_load(f)
            
        parts = filepath.split('/')
        if len(parts) < 2:
            logger.warning(f"Неверный путь {client_ip}: {filepath}")
            abort(404)
            
        main_dir, subdir = parts[:2]
        
        if main_dir not in links or subdir not in links[main_dir]:
            logger.warning(f"Неверный путь {client_ip}: {filepath}")
            abort(404)
            
        if len(parts) == 2:
            logger.info(f"Открытие каталога {main_dir}/{subdir} для {client_ip}")
            return send_from_directory(os.path.join('.', main_dir), subdir)
        
        file_path = '/'.join(parts[2:])
        logger.info(f"Открытие каталога {file_path} для {client_ip}")
        return send_from_directory(os.path.join('.', main_dir, subdir), file_path)
    
    except Exception as e:
        logger.error(f"Ошибка запроса от {client_ip}: {str(e)}")
        abort(403)

if __name__ == '__main__':
    settings = load_config()
    
    if settings.getboolean('sync_on_startup', False):
        logger.info("Включена синхронизация при запуске")
        sync_files()
        
    if settings.getboolean('enable_scheduled_sync', True):
        logger.info("Включена синхронизация по графику")
        schedule_sync()
        
    app.run(host='0.0.0.0', port=3000)