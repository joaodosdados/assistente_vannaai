# Assistente MVP (FastAPI + Postgres + Vanna)

Este repositório contém um **MVP de assistente** para consulta de status de processos usando:
- **FastAPI** (backend leve)
- **Postgres** (armazenamento determinístico dos processos)
- **Vanna.ai** (opcional, geração de SQL em linguagem natural)
- **uv** (gerenciador de dependências)

---

## 🚀 1. Pré-requisitos

- macOS  
- [Postgres.app](https://postgresapp.com/) (ou `brew install postgresql@17`)  
- Python 3.11+  
- [uv](https://docs.astral.sh/uv/) (`brew install uv`)  

Confirme:
```bash
psql --version
uv --version
python --version
```

---

## 🛠️ 2. Preparar ambiente Python

Na raiz do projeto:

```bash
uv init
uv sync
```

Isso cria `.venv/` e instala dependências listadas no `pyproject.toml`.

Para rodar comandos dentro do ambiente:
```bash
uv run <comando>
```

Exemplo:
```bash
uv run uvicorn app.main:app --reload --port 8000
```

---

## 🗄️ 3. Banco de dados

### Criar banco
```bash
createdb processos
```

### Inicializar schema, views e dados
Use o script único `init.sql`:

```bash
psql -d processos -f sql/init.sql
```

Isso cria:
- Tabela `public.processo`
- Schema `assistente`
- Views `vw_processo` e `vw_evento_processo`
- Seeds (`id_processo` 123 e 456)

---

## ⚙️ 4. Configuração da API

Crie o arquivo `config/.env` com as credenciais locais:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=processos
DB_USER=joaolso    # seu usuário macOS
DB_PASSWORD=
DB_SSLMODE=disable
```

---

## ▶️ 5. Rodar API

Na raiz do projeto:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

A API sobe em [http://localhost:8000](http://localhost:8000)

---

## 🧪 6. Testar endpoints

### Status determinístico (template SQL)
```bash
curl -X POST http://localhost:8000/status/consultar   -H "Content-Type: application/json"   -d '{"id_processo":"123"}'
```

Resposta esperada:
```json
{
  "result": [
    {
      "status_atual": "Em análise",
      "etapa_atual": "Validação documental",
      "dt_ult_atualizacao": "2025-08-31T14:12:00"
    }
  ],
  "source": "assistente.vw_processo"
}
```

### Consulta em linguagem natural (opcional, Vanna)
```bash
curl -X POST http://localhost:8000/nlq   -H "Content-Type: application/json"   -d '{"question":"mostrar status_atual e etapa_atual do processo 123 na assistente.vw_processo"}'
```

---

## 📂 Estrutura de diretórios

```
assistente-mvp/
├─ app/
│  ├─ main.py              # FastAPI entrypoint
│  ├─ config.py            # lê variáveis .env
│  ├─ db.py                # conexão Postgres
│  ├─ guardrails.py        # regras de SQL seguro
│  ├─ schemas.py           # modelos Pydantic
│  ├─ routers/
│  │  ├─ status.py         # /status/consultar
│  │  └─ nlq.py            # /nlq (com Vanna)
│  └─ services/
│     └─ vanna_client.py   # inicialização do Vanna
├─ config/.env.example
├─ sql/init.sql            # cria schema + views + seed
├─ pyproject.toml          # gerenciado pelo uv
└─ README.md
```

---

## 🔒 Notas de segurança

- Os CPFs são mascarados nas views (`123***01`).  
- O usuário do banco usado no MVP tem privilégios completos (seu usuário macOS).  
- Para produção, recomenda-se criar um **role somente leitura** (`role_assistente_ro`) e usar na API.

---

## ✅ Roadmap de evolução

- [ ] Adicionar autenticação (OAuth2 / JWT)  
- [ ] Criar role `role_assistente_ro` e apontar API para ela  
- [ ] Logging e métricas (Prometheus/Grafana)  
- [ ] Novos endpoints: atualizar contato, enviar documentos, etc.  
- [ ] Deploy containerizado (quando Docker for liberado)

---
