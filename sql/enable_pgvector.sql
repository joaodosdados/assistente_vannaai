-- enable_pgvector.sql
-- Habilita a extensão pgvector no banco atual (PostgreSQL 15+)
-- Rode com: psql -d processos -f sql/enable_pgvector.sql

CREATE EXTENSION IF NOT EXISTS vector;

-- Opcional: índices para busca aproximada podem ser criados depois que a tabela de embeddings tiver dados.
-- Exemplo (ajuste nomes conforme as tabelas criadas pelo Vanna):
-- CREATE INDEX IF NOT EXISTS idx_vanna_chunks_embedding
--   ON vanna_chunks USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
