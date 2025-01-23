import os
from dotenv import load_dotenv

# Nạp thông tin cấu hình từ file .env
load_dotenv()

def get_db_config():
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME")
    }

def get_api_config():
    return {
        "api_url": os.getenv("API_URL")
    }
