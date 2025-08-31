# Arquitetura

- API: FastAPI (endpoints `/chat` e `/nlq`)
- Banco: Postgres com schema `assistente` (views) e `vanna` (pgvector)
- NLQ: Vanna + Ollama (LLaMA3) para fallback
- Guardrails: enforce_limit, is_sql_safe, coerce_types
