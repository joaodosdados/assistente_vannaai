-- ============================================================
-- Assistente MVP - init.sql
-- Cria schema, tabela, views, índices e dados de exemplo
-- Compatível com PostgreSQL 15+
-- ============================================================

-- 1) Schema dedicado ao assistente
CREATE SCHEMA IF NOT EXISTS assistente;

-- 2) Tabela base (simples) de processos
CREATE TABLE IF NOT EXISTS public.processo (
  id_processo           VARCHAR PRIMARY KEY,
  cpf                   VARCHAR(11)      NOT NULL,
  status_atual          VARCHAR(50)      NOT NULL,
  etapa_atual           VARCHAR(50)      NOT NULL,
  dt_ult_atualizacao    TIMESTAMP        NOT NULL DEFAULT now()
);

-- 3) Índices úteis (buscas por id/CPF)
CREATE INDEX IF NOT EXISTS idx_processo_id        ON public.processo (id_processo);
CREATE INDEX IF NOT EXISTS idx_processo_cpf       ON public.processo (cpf);
CREATE INDEX IF NOT EXISTS idx_processo_status    ON public.processo (status_atual);
CREATE INDEX IF NOT EXISTS idx_processo_etapa     ON public.processo (etapa_atual);
CREATE INDEX IF NOT EXISTS idx_processo_dt        ON public.processo (dt_ult_atualizacao);

-- 4) Views seguras no schema `assistente`
--    Observação: mascaramos CPF para evitar exposição de PII
CREATE OR REPLACE VIEW assistente.vw_processo AS
SELECT
  p.id_processo,
  LEFT(p.cpf, 3) || '***' || RIGHT(p.cpf, 2) AS cpf_mask,
  p.status_atual,
  p.etapa_atual,
  p.dt_ult_atualizacao
FROM public.processo p;

CREATE OR REPLACE VIEW assistente.vw_evento_processo AS
SELECT
  p.id_processo,
  p.etapa_atual      AS etapa,
  p.status_atual     AS status,
  p.dt_ult_atualizacao AS dt_evento,
  NULL::text         AS obs
FROM public.processo p;

-- 5) Seeds (dados de exemplo)
INSERT INTO public.processo (id_processo, cpf, status_atual, etapa_atual)
VALUES
  ('123', '12345678901', 'Em análise',         'Validação documental'),
  ('456', '98765432100', 'Aguardando cliente', 'Envio de documentos')
ON CONFLICT (id_processo) DO NOTHING;

-- 6) (Opcional) Role somente leitura para o assistente
--    Se sua TI permitir criar role/senha no dev local, descomente abaixo.
-- DO $$
-- BEGIN
--   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_assistente_ro') THEN
--     CREATE ROLE role_assistente_ro LOGIN PASSWORD 'mvp_ro_password';
--   END IF;
-- END $$;

-- GRANT USAGE ON SCHEMA assistente TO role_assistente_ro;
-- GRANT SELECT ON ALL TABLES IN SCHEMA assistente TO role_assistente_ro;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA assistente
--   GRANT SELECT ON TABLES TO role_assistente_ro;

-- 7) Verificações rápidas (não atrapalham automação)
-- \echo '---- Conteúdo vw_processo ----'
-- SELECT * FROM assistente.vw_processo LIMIT 5;
-- \echo '---- Conteúdo vw_evento_processo ----'
-- SELECT * FROM assistente.vw_evento_processo LIMIT 5;

-- Fim do init.sql