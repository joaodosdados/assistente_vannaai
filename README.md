# Assistente VANNAAI

MVP de um **assistente em linguagem natural** para consulta de processos.  
API em **FastAPI**, banco **Postgres** com **views seguras** e integração opcional com **VannaAI** para NLQ (natural language queries).

## 🚀 Subir a API
```bash
uv run uvicorn app.main:app --reload --port 8000
# OpenAPI: http://localhost:8000/docs
```

## 🧪 Testar consultas

### Pergunta em linguagem natural
Em outro terminal:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"qual o andamento do meu processo 123"}'
```

### Consulta direta de status
```bash
curl -X POST http://localhost:8000/status/consultar \
  -H "Content-Type: application/json" \
  -d '{"id_processo":"123"}'
```

## 📚 Documentação completa
Guia de instalação, arquitetura, segurança e integrações:  
👉 [Docs (MkDocs)](https://joaodosdados.github.io/assistente_vannaai) *(ou rode `mkdocs serve` localmente)*
