# Deploy com Docker Compose

## Subindo tudo
```bash
docker compose up -d
docker compose logs -f
```

- Serviço **db**: `postgres:14`, volume `db_data`, seed via `sql/init.sql`.
- Serviço **api**: build local, expõe `8000` → `http://localhost:8000/docs`

## Encerrando
```bash
docker compose down -v
```

> Dica: em dev, monte o diretório do projeto como volume para *live reload*.
