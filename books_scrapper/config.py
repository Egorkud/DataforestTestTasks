import os

from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv()


class Config:
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # Scraping
    MAX_WORKER_THREADS = int(os.getenv('MAX_WORKER_THREADS'))
    USER_AGENT = UserAgent().random

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
