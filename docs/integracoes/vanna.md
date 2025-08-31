# Integração com Vanna (opcional)

A integração converte perguntas em PT‑BR em **SQL**. Fluxo:
1. Recebe `question`.
2. Gera SQL candidato (prompt engineering e few-shots específicos do schema).
3. Passa pelo **validador** (guardrails).
4. Se aprovado, executa em `assistente.*`.

## Configuração
- Habilite via variável de ambiente (ex.: `ENABLE_VANNA=true`).
- Configure credenciais/chaves conforme a lib usada.

## Boas práticas
- **Few-shots** devem usar **views** do schema `assistente`.
- Dê nomes autoexplicativos às colunas das views.
- Mantenha um conjunto de **perguntas de regressão** para testes.

## Limitações típicas
- Ambiguidade sem contexto.
- Joins não triviais entre views.
- Datas relativas (“última semana”) exigem normalização.
