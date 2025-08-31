# app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# carrega SEMPRE o .env de config/.env
ENV_PATH = Path(__file__).resolve().parents[1] / "config" / ".env"
load_dotenv(dotenv_path=str(ENV_PATH))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "processos")
DB_USER = os.getenv("DB_USER", "")  # <- não pode ficar vazio
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # <- não pode ficar vazio
DB_SSLMODE = os.getenv("DB_SSLMODE", "disable")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
STATEMENT_TIMEOUT_MS = int(os.getenv("STATEMENT_TIMEOUT_MS", "4000"))
