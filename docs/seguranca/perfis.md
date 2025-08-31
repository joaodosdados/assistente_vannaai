# Perfis de acesso (roles)

## Desenvolvimento
- Usuário app com permissões de leitura no schema `assistente`.
- Permissões de escrita usadas apenas por scripts de **seed**.

## Produção (recomendado)
- `role_assistente_ro`: `USAGE` no schema `assistente` e `SELECT` nas views.
- Usuário da API pertence apenas a `role_assistente_ro`.
- Sem privilégios de escrita/tabelas base.

### Exemplo (ajuste para seu ambiente)
```sql
-- criar role somente leitura
CREATE ROLE role_assistente_ro;
GRANT USAGE ON SCHEMA assistente TO role_assistente_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA assistente TO role_assistente_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA assistente GRANT SELECT ON TABLES TO role_assistente_ro;

-- vincular usuário da API
GRANT role_assistente_ro TO usuario_api;
```
