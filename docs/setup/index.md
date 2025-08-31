# Setup do ambiente

!!! info "Pré-requisitos"
    - Python 3.11+
    - Postgres 14+
    - `uv` (gerenciador de dependências Python)
    - (Opcional) Docker + Docker Compose

## macOS
```bash
# Postgres (Homebrew) e uv
brew install postgresql@14
brew services start postgresql@14

# Banco e seed
createdb processos
psql -d processos -f sql/init.sql

# Dependências
uv sync

# Executar API
uv run uvicorn app.main:app --reload --port 8000
# OpenAPI: http://localhost:8000/docs
```

## Windows (WSL2 recomendado)
1. Instale **WSL2 + Ubuntu** pela Microsoft Store.
2. Dentro do Ubuntu:
```bash
sudo apt update && sudo apt install -y postgresql postgresql-contrib python3.11 python3.11-venv pipx
sudo -u postgres createuser -s $USER || true
createdb processos
psql -d processos -f sql/init.sql

pipx install uv
uv sync
uv run uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

## Windows (sem WSL)
- Instale Postgres pelo instalador oficial (incluir `psql` no PATH), Python 3.11 e `pipx`.
- `pipx install uv`
- Siga os mesmos comandos de **sync** e **execução** acima.

## Variáveis de ambiente
Crie um `.env` na raiz (apenas se usar conexão customizada):
```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/processos
APP_ENV=dev
LOG_LEVEL=INFO
```
Se ausente, a app usa valores padrão do `settings`.
