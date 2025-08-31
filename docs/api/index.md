# API (FastAPI)

- **OpenAPI**: `http://localhost:8000/docs`

## POST `/status/consultar`
Obtém status do processo por `id_processo`.

**Body**
```json
{"id_processo": "123"}
```

**Resposta (exemplo)**
```json
{
  "result": [
    {
      "id_processo": "123",
      "status_atual": "Em análise",
      "etapa_atual": "Validação documental",
      "dt_ult_atualizacao": "2025-08-31T14:12:00"
    }
  ],
  "source": "assistente.vw_processo"
}
```

## POST `/nlq` (opcional)
Pergunta em linguagem natural (PT‑BR) → SQL sugerido pelo Vanna → validado por guardrails e executado em **views**.

**Body**
```json
{"question": "mostrar status_atual e etapa_atual do processo 123"}
```

**Resposta (exemplo)**
```json
{
  "result": [
    {"status_atual": "Em análise", "etapa_atual": "Validação documental"}
  ],
  "source": "assistente.vw_processo"
}
```

> Notas:
> - Em dev, o NLQ pode ser desabilitado e você usa SQL estático.
> - Em prod, os **guardrails** são obrigatórios.
