from vanna.ollama import Ollama
from vanna.pgvector import PG_VectorStore
from .. import config


def _make_dsn() -> str:
    # formato SQLAlchemy/psycopg3:
    # postgresql+psycopg://user:password@host:port/dbname
    pwd = config.DB_PASSWORD or ""
    return f"postgresql+psycopg://{config.DB_USER}:{pwd}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"


class VannaOllamaPgVector(Ollama, PG_VectorStore):
    def __init__(self, config_dict=None):
        Ollama.__init__(self, config=config_dict)
        PG_VectorStore.__init__(self, config=config_dict)


def build_vanna() -> VannaOllamaPgVector:
    cfg = {
        # LLM (Ollama)
        "schema": "vanna",
        "model": config.OLLAMA_MODEL,
        "base_url": config.OLLAMA_BASE_URL,
        # Vetor no Postgres
        "connection_string": _make_dsn(),
        # Coleções (tabelas) utilizadas pelo Vanna
        "ddl_collection": "vanna_ddl",
        "sql_collection": "vanna_sql",
        "documentation_collection": "vanna_docs",
        # 🔹 Embeddings (HuggingFace via LangChain)
        "embedding_provider": "huggingface",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        # modelos alternativos mais robustos:
        # "sentence-transformers/all-MiniLM-L12-v2"
        # "sentence-transformers/all-mpnet-base-v2"
    }
    return VannaOllamaPgVector(config_dict=cfg)


def connect_and_seed(vn: VannaOllamaPgVector) -> None:
    vn.connect_to_postgres(
        host=config.DB_HOST,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT,
    )

    ddl = """
    CREATE OR REPLACE VIEW assistente.vw_processo AS
    SELECT
      p.id_processo,
      LEFT(p.cpf, 3) || '***' || RIGHT(p.cpf, 2) AS cpf_mask,
      p.status_atual,
      p.etapa_atual,
      p.dt_ult_atualizacao
    FROM public.processo p;

    CREATE OR REPLACE VIEW assistente.vw_evento_processo AS
    SELECT
      p.id_processo,
      p.etapa_atual      AS etapa,
      p.status_atual     AS status,
      p.dt_ult_atualizacao AS dt_evento,
      NULL::text         AS obs
    FROM public.processo p;
    """
    try:
        vn.train(ddl=ddl)
    except Exception as e:
        print(f"[VANNA] Aviso ao treinar DDL: {e}")

    # 👇 exemplos few-shot para reforçar padrão
    try:
        vn.train(
            sql="SELECT status_atual, etapa_atual FROM assistente.vw_processo WHERE id_processo = '123';",
            question="mostrar status_atual e etapa_atual do processo 123 na assistente.vw_processo",
        )
        vn.train(
            sql="SELECT status_atual, etapa_atual FROM assistente.vw_processo WHERE id_processo = '456';",
            question="status e etapa do processo 456",
        )
    except Exception as e:
        print(f"[VANNA] Aviso ao treinar exemplo: {e}")


def generate_sql(vn: VannaOllamaPgVector, question: str) -> str:
    return vn.generate_sql(question)
