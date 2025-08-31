from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import re
from ..db import get_conn
from ..services.vanna_client import generate_sql

router = APIRouter(prefix="/chat", tags=["chat"])

# --------- helpers NLU simples ----------
RE_PROC = re.compile(r"\b(\d{3,20})\b")  # ex: "123", "2024-000123" (ajuste se precisar)
RE_CPF = re.compile(r"\b(\d{3}\.?\d{3}\.?\d{3}-?\d{2})\b")


def detect_intent(msg: str) -> str:
    m = msg.lower()
    # palavras-chave comuns em PT-BR
    if ("processo" in m or "protocolo" in m or "pedido" in m) and (
        "status" in m
        or "situação" in m
        or "situacao" in m
        or "andamento" in m
        or "como está" in m
        or "como ta" in m
    ):
        return "status_processo"
    # adicione outras intenções (“prazo”, “documentos faltantes”, etc.)
    return "fallback_nlq"


def extract_ids(msg: str):
    cpf = None
    mcpf = RE_CPF.search(msg)
    if mcpf:
        cpf = re.sub(r"\D", "", mcpf.group(1))  # apenas números
    proc = None
    mproc = RE_PROC.search(msg)
    if mproc:
        proc = mproc.group(1)
    return proc, cpf


# --------- schema ----------
class ChatIn(BaseModel):
    message: str


# --------- rota ----------
@router.post("")
def chat(payload: ChatIn, request: Request):
    msg = payload.message.strip()
    intent = detect_intent(msg)

    if intent == "status_processo":
        id_processo, cpf = extract_ids(msg)
        if not id_processo and not cpf:
            raise HTTPException(
                status_code=400, detail="Me informe o número do processo ou CPF."
            )

        # SQL determinístico e seguro
        try:
            with get_conn() as conn, conn.cursor() as cur:
                if id_processo:
                    cur.execute(
                        """
                        SELECT status_atual, etapa_atual, dt_ult_atualizacao
                        FROM assistente.vw_processo
                        WHERE id_processo = %s
                        """,
                        (id_processo,),
                    )
                else:
                    # exemplo se quiser buscar pelo CPF original (se existir coluna/normalização)
                    cur.execute(
                        """
                        SELECT status_atual, etapa_atual, dt_ult_atualizacao
                        FROM assistente.vw_processo
                        WHERE REPLACE(REPLACE(REPLACE(cpf_mask, '*',''),'.',''),'-','') LIKE %s
                        """,
                        (
                            f"{cpf[:3]}%",
                        ),  # simplão só pra demo; melhor ter um índice/coluna cpf_normalizado
                    )
                row = cur.fetchone()
                if not row:
                    return {
                        "answer": "Não encontrei este processo. Confirme o número/CPF."
                    }
                status_atual, etapa_atual, dt_ult = row
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Erro ao consultar processo: {e}"
            )

        # resposta natural em PT-BR
        dt = dt_ult.strftime("%d/%m/%Y %H:%M") if dt_ult else "—"
        return {
            "answer": f"O processo {id_processo or cpf} está **{status_atual}** na etapa **{etapa_atual}** (última atualização em {dt})."
        }

    # -------- fallback → NLQ com guardrails --------
    vn = getattr(request.app.state, "vanna", None)
    if vn is None:
        raise HTTPException(status_code=503, detail="Assistente NLQ não inicializado")

    sql = generate_sql(vn, msg)

    # aplique seus guardrails existentes (coerce_types, is_sql_safe, enforce_limit)
    from ..guardrails import coerce_types, is_sql_safe, enforce_limit

    sql = coerce_types(sql)
    if not is_sql_safe(sql):
        raise HTTPException(
            status_code=400, detail="Consulta não permitida pelas políticas."
        )
    sql = enforce_limit(sql)

    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [c.name for c in cur.description]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar SQL: {e}")

    # formate uma resposta amigável (ex.: 1ª linha)
    if rows:
        preview = dict(zip(cols, rows[0]))
        return {"answer": f"Encontrei isto: {preview}", "sql": sql}
    return {"answer": "Não encontrei resultados.", "sql": sql}
