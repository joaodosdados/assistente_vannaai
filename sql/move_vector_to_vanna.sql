-- sql/move_vector_to_vanna.sql
-- Alternativa recomendada: mover/centralizar o vector store para o schema 'vanna'
-- Execute como superuser no DB 'processos'.

CREATE SCHEMA IF NOT EXISTS vanna AUTHORIZATION vanna;
GRANT USAGE, CREATE ON SCHEMA vanna TO vanna;

-- Mover tabelas se elas existirem no public
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'public' AND c.relname = 'langchain_pg_collection' AND c.relkind = 'r') THEN
    ALTER TABLE public.langchain_pg_collection SET SCHEMA vanna;
  END IF;

  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'public' AND c.relname = 'langchain_pg_embedding' AND c.relkind = 'r') THEN
    ALTER TABLE public.langchain_pg_embedding SET SCHEMA vanna;
  END IF;

  -- Mover sequence se existir
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'public' AND c.relname = 'langchain_pg_embedding_id_seq' AND c.relkind = 'S') THEN
    ALTER SEQUENCE public.langchain_pg_embedding_id_seq SET SCHEMA vanna;
  END IF;
END $$;

-- Transferir ownership para o usuário de app
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'vanna' AND c.relname = 'langchain_pg_collection' AND c.relkind = 'r') THEN
    ALTER TABLE vanna.langchain_pg_collection OWNER TO vanna;
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE vanna.langchain_pg_collection TO vanna;
  END IF;

  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'vanna' AND c.relname = 'langchain_pg_embedding' AND c.relkind = 'r') THEN
    ALTER TABLE vanna.langchain_pg_embedding OWNER TO vanna;
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE vanna.langchain_pg_embedding TO vanna;
  END IF;

  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'vanna' AND c.relname = 'langchain_pg_embedding_id_seq' AND c.relkind = 'S') THEN
    ALTER SEQUENCE vanna.langchain_pg_embedding_id_seq OWNER TO vanna;
    GRANT USAGE, SELECT ON SEQUENCE vanna.langchain_pg_embedding_id_seq TO vanna;
  END IF;
END $$;

-- Garantir search_path para o usuário vanna (aponta primeiro para o schema vanna)
ALTER ROLE vanna IN DATABASE processos SET search_path TO vanna,public;

-- Defaults para objetos futuros no schema vanna
ALTER DEFAULT PRIVILEGES IN SCHEMA vanna GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vanna;
ALTER DEFAULT PRIVILEGES IN SCHEMA vanna GRANT USAGE, SELECT ON SEQUENCES TO vanna;
