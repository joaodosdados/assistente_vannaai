# Interface de Treinamento (Admin)

- Acesse: `/admin/treinamento`
- Seções:
  - **Treinar via INFORMATION_SCHEMA**: opcionalmente filtre por tabelas (separadas por vírgula).
  - **Treinar DDL/Documentação/SQL**: cole trechos para enriquecer o RAG.
  - **Perguntar**: gere SQL a partir de linguagem natural e veja o resultado.

Os endpoints usam os mesmos **guardrails** (somente SELECT, schema `assistente`). Baseado nas diretrizes oficiais do Vanna para **Other LLM / Other VectorDB** e **OpenAI + Chroma**.
