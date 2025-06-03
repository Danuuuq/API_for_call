import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from app.core.config import settings

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FORMAT = settings.log_format

def setup_logger(name: str, level=logging.INFO):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"{name}.log")

    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",       # каждый день в полночь
        interval=1,
        backupCount=7,         # сколько логов хранить
        encoding="utf-8",
        utc=False              # True, если хочешь по UTC
    )
    handler.suffix = "%Y-%m-%d"  # добавит дату к имени при ротации
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

def setup_logger_v2(name: str, level=logging.INFO):
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'{name}_{date_str}.log'
    path = os.path.join(LOG_DIR, filename)
    handlers = RotatingFileHandler(path, maxBytes=10**6, backupCount=3)
    handlers.setFormatter(logging.Formatter(LOG_FORMAT))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handlers)
    return logger

db_logger = setup_logger('db_log', logging.INFO)
action_url_logger = setup_logger('action_url', logging.INFO)
