# app/vanna_integration.py
import os
from urllib.parse import urlparse

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
if LLM_PROVIDER == "openai":
    from vanna.openai import OpenAI_Chat as ChatBackend
else:
    from vanna.ollama import Ollama as ChatBackend

from vanna.pgvector import PG_VectorStore


class MyVanna(PG_VectorStore, ChatBackend):
    def __init__(self, config=None):
        PG_VectorStore.__init__(self, config=config)
        ChatBackend.__init__(self, config=config)


def _pg_conn_kwargs_from_url(url: str):
    p = urlparse(url)
    return {
        "host": p.hostname or "localhost",
        "dbname": (p.path or "/").lstrip("/") or "postgres",
        "user": p.username or "postgres",
        "password": p.password or "",
        "port": p.port or 5432,
    }


def get_vanna():
    db_url = os.getenv(
        "DATABASE_URL", "postgresql://vanna:vanna@localhost:5432/processos"
    )
    cfg = {
        "connection_string": db_url,
        "schema": os.getenv("VANNA_SCHEMA", "public"),
        "table": os.getenv("VANNA_TABLE", "vanna_embeddings"),
        "model": os.getenv("OLLAMA_MODEL", "llama3.1"),
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        if LLM_PROVIDER != "openai"
        else None,
        "api_key": os.getenv("OPENAI_API_KEY") if LLM_PROVIDER == "openai" else None,
        "pgvector_connection_string": db_url,
        "pgvector_schema": os.getenv("VANNA_SCHEMA", "public"),
        "pgvector_table": os.getenv("VANNA_TABLE", "vanna_embeddings"),
    }
    if LLM_PROVIDER == "openai":
        cfg["model"] = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    else:
        cfg["model"] = os.getenv("OLLAMA_MODEL", "llama3.1")
    vn = MyVanna(config=cfg)
    vn.connect_to_postgres(**_pg_conn_kwargs_from_url(db_url))
    return vn
