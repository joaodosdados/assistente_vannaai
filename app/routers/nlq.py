from fastapi import APIRouter, HTTPException, Request
from ..schemas import NLQ
from ..db import get_conn
from ..guardrails import is_sql_safe, enforce_limit, coerce_types
from ..services.vanna_client import generate_sql
import traceback

router = APIRouter(prefix="/nlq", tags=["nlq"])


@router.post("")
def nlq(payload: NLQ, request: Request):
    vn = getattr(request.app.state, "vanna", None)
    if vn is None:
        raise HTTPException(status_code=503, detail="Vanna não inicializado")

    sql = generate_sql(vn, payload.question)
    sql = coerce_types(sql)  # 👈 novo
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
        tb = traceback.format_exc()
        # psycopg3: alguns erros tem .sqlstate
        sqlstate = getattr(e, "sqlstate", None)
        print(f"[NLQ ERROR] sqlstate={sqlstate} err={e}\n{tb}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar SQL: {e}")

    return {"sql": sql, "result": [dict(zip(cols, r)) for r in rows]}
