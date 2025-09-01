-- setup_pgvector_local.sql
-- Cria usuário, banco e habilita a extensão 'vector' para uso do Vanna (pgvector).
-- Execute este arquivo conectado como superuser (ex.: 'postgres').

-- 1) Usuário de app
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'vanna') THEN
      CREATE ROLE vanna WITH LOGIN PASSWORD 'vanna';
   END IF;
END$$;

-- 2) Banco de dados (se quiser criar do zero e já deixar o dono = vanna)
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'processos') THEN
      CREATE DATABASE processos OWNER vanna;
   END IF;
END$$;

-- 3) Habilitar extensão pgvector no DB 'processos'
--    OBS: esta parte precisa ser rodada DENTRO do DB 'processos'
-- \connect processos
-- CREATE EXTENSION IF NOT EXISTS vector;

-- 4) (Opcional) Garantir privilégios para o usuário vanna no schema 'public'
-- \connect processos
-- GRANT USAGE ON SCHEMA public TO vanna;
-- GRANT CREATE ON SCHEMA public TO vanna;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vanna;
