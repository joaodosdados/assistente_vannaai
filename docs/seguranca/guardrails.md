# Guardrails de SQL

## Políticas
- **Somente `SELECT`** é permitido.
- **Somente views** do schema **`assistente`** podem ser acessadas.
- **Proibido**: DDL/DML (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`), `COPY`, `CREATE`, `GRANT`, etc.
- **Proibido**: acesso a outros schemas (`public`, `pg_catalog`, `information_schema`, ...).
- **Proibido**: funções perigosas, `;` múltiplos statements, CTEs que escapem da policy.
- **LIMIT** padrão pode ser aplicado (ex.: 500) para evitar resultados gigantes.

## Estratégia de validação
1. Parse do SQL (AST) para garantir somente `SELECT`.
2. Lista branca de objetos: `assistente.vw_*`.
3. *Static checks* (schema, funções, múltiplas instruções).
4. *Runtime checks* (timeout, row limit).

## Exemplos
Pergunta segura:
> "listar `status_atual`, `etapa_atual` do processo 123"

Pergunta bloqueada:
> "apague a tabela processo" → DDL/DML proibido.
