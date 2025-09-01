-- sql/grant_vector_in_public.sql
-- Caso as tabelas langchain_pg_* tenham sido criadas no schema public
-- e pertençam a outro owner, este script garante acesso ao usuário 'vanna'.
-- Execute como superuser no DB 'processos'.

GRANT USAGE ON SCHEMA public TO vanna;

-- Permissões nas tabelas já existentes no public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.langchain_pg_collection TO vanna;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.langchain_pg_embedding TO vanna;

-- Se existirem sequences associadas (ex.: id bigserial em embedding):
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE c.relkind = 'S' AND n.nspname = 'public' AND c.relname = 'langchain_pg_embedding_id_seq') THEN
    GRANT USAGE, SELECT ON SEQUENCE public.langchain_pg_embedding_id_seq TO vanna;
  END IF;
END $$;

-- Defaults para novos objetos criados por quem rodar este comando no schema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vanna;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO vanna;
