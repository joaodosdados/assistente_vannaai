-- grant_assistente_read.sql
-- Concede ao usuário 'vanna' permissão para consultar as views do schema `assistente`
-- e as tabelas subjacentes necessárias (no seu caso, public.processo).
-- Execute no DB `processos` como superuser (ex.: postgres).

-- 1) Permissões no schema e nas views do schema `assistente`
GRANT USAGE ON SCHEMA assistente TO vanna;
GRANT SELECT ON ALL TABLES IN SCHEMA assistente TO vanna;

-- Garantir que futuras views/tabelas em `assistente` também fiquem legíveis
ALTER DEFAULT PRIVILEGES IN SCHEMA assistente GRANT SELECT ON TABLES TO vanna;

-- 2) Permissões nas tabelas base referenciadas pelas views
--    (por padrão, views NÃO "encapsulam" privilégios; o usuário precisa enxergar a base)
GRANT SELECT ON TABLE public.processo TO vanna;
