# Observabilidade

## Logs
- **Níveis**: `DEBUG` | `INFO` | `WARNING` | `ERROR`
- Configure via `LOG_LEVEL` no `.env`.
- Registre:
  - ID de correlação por requisição.
  - Nome da view consultada (`source`).
  - Duração da consulta e nº de linhas retornadas (sem dados sensíveis).

## Saúde
- Endpoint `/healthz` (sugerido) para verificar conexão com DB.
- Timeout de query configurável (ex.: 10s).

## Futuro
- Expor métricas Prometheus (latência, throughput, erros).
