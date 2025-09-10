import os
from dotenv import load_dotenv

load_dotenv()


# --- Configuration ---

# --- Ollama ---
OLLAMA_URL = os.getenv("OLLAMA_URL")  # URL подключения к ии
MODEL_NAME = os.getenv("MODEL_NAME")  # Модель

# --- Bot ---
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен бота

# --- Redis ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CONTEXT_TTL = int(os.getenv("CONTEXT_TTL", 3600))  # 1 час

# --- Image ---
THUMBNAIL_URL = os.getenv("THUMBNAIL_URL")

# --- memory ---
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", 20))  # Максимум сообщений в контексте (после system) По умолчанию 20
