# Arquitetura do MVP

```mermaid
flowchart LR
User[Usuário / Cliente] -->|HTTP JSON| FastAPI[FastAPI]
FastAPI -->|SQL (psycopg/asyncpg)| Postgres[(Postgres)]
subgraph NLQ (opcional)
FastAPI --> Vanna[VannaAI]
Vanna -->|SQL gerado| Guardrails[Guardrails de SQL]
Guardrails -->|SQL seguro| Postgres
end
Postgres --> Views[Views de leitura: schema assistente]
```

- **FastAPI** expõe endpoints REST.
- **Postgres** armazena tabelas base e **views** no schema `assistente` para leitura segura.
- **Vanna (opcional)** sugere SQL a partir de linguagem natural.
- **Guardrails** validam/limitam o SQL (somente `SELECT` em views aprovadas).

## Fluxos principais

### `/status/consultar`
1. Recebe `id_processo`.
2. Executa `SELECT` em `assistente.vw_processo`.
3. Retorna `status_atual`, `etapa_atual`, `dt_ult_atualizacao`, `source`.

### `/nlq` (opcional)
1. Recebe `question` em PT‑BR.
2. Vanna propõe SQL.
3. Guardrails validam (DDL/DML, schemas, funções).
4. Executa em view do schema `assistente` e retorna resultado + `source`.
