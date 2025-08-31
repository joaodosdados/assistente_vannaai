# Fluxo NLQ

1. Recebe pergunta em linguagem natural
2. Monta prompt com DDL das views
3. Passa para o LLM (Ollama)
4. SQL gerado
5. Guardrails aplicados
6. Executa no Postgres
