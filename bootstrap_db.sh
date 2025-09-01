#!/usr/bin/env bash
set -euo pipefail

# Use este script em macOS/Linux com psql disponível.
# Ele vai:
# 1) criar role 'vanna' (se não existir)
# 2) criar DB 'processos' (se não existir) com owner = vanna
# 3) habilitar a extensão 'vector' no DB 'processos'

# Ajuste se necessário:
PG_SUPERUSER="${PG_SUPERUSER:-postgres}"
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PGPASSWORD="${PGPASSWORD:-}"

echo "[1/3] Aplicando setup de role/DB (como superuser ${PG_SUPERUSER})"
psql "postgresql://${PG_SUPERUSER}@${PG_HOST}:${PG_PORT}/postgres" -f setup_pgvector_local.sql

echo "[2/3] Habilitando extensão vector em 'processos'"
psql "postgresql://${PG_SUPERUSER}@${PG_HOST}:${PG_PORT}/processos" -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "[3/3] Pronto. Configure seu .env com:"
echo "DATABASE_URL=postgresql://vanna:vanna@${PG_HOST}:${PG_PORT}/processos"
