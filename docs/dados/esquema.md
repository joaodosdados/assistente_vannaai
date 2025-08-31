# Esquema, tabelas e views

## Esquema base
- **Tabela**: `public.processo`
- **Tabela**: `public.evento_processo`

Essas tabelas representam o processo e seus eventos/alterações.

## Views de leitura (schema `assistente`)
- **`assistente.vw_processo`**
  - Colunas: `id_processo`, `status_atual`, `etapa_atual`, `dt_ult_atualizacao`, `cpf_mascarado`, ...
  - Aplica **mascaramento de PII** (ex.: CPF formatado `123***01`).

- **`assistente.vw_evento_processo`**
  - Colunas: `id_processo`, `evento`, `descricao`, `data_evento`

> As **views** são a superfície autorizada para consultas. A API não deve consultar tabelas diretamente em produção.

## Inicialização do banco
```bash
psql -d processos -f sql/init.sql
```
O script cria as tabelas e views com alguns dados de exemplo.

## Convenções
- Todas as consultas da API devem usar o **schema `assistente`**.
- Evitar PII nos retornos; quando necessário, aplicar mascaramento nas views.
