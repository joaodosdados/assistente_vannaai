from fastapi import APIRouter, HTTPException
from ..db import get_conn
from ..schemas import StatusIn

router = APIRouter(prefix="/status", tags=["status"])

STATUS_SQL = """
SELECT status_atual, etapa_atual, dt_ult_atualizacao
FROM assistente.vw_processo
WHERE id_processo = %(id_processo)s
"""


@router.post("/consultar")
def consultar(payload: StatusIn):
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(STATUS_SQL, {"id_processo": payload.id_processo})
            rows = cur.fetchall()
            cols = [c.name for c in cur.description]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "result": [dict(zip(cols, r)) for r in rows],
        "source": "assistente.vw_processo",
    }
