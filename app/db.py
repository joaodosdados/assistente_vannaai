import psycopg
from . import config


def get_conn():
    return psycopg.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        options=f"-c statement_timeout={config.STATEMENT_TIMEOUT_MS}",
    )
