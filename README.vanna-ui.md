# Branch: vanna-ui

Interface administrativa para treinar Vanna (INFORMATION_SCHEMA, DDL, docs, SQL) e perguntar via NLQ, conectada ao Postgres e com guardrails.

## Como habilitar no FastAPI
No `app/main.py`:
```python
from app.ui.router import router as ui_router
app.include_router(ui_router)
```

Suba a API e acesse: `http://localhost:8000/admin/treinamento`.
