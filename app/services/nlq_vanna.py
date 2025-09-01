# app/services/nlq_vanna.py
from typing import Optional, List, Dict, Any
from app.vanna_integration import get_vanna
from app.guardrails.sql_guard import validate_sql

_vn = None
def _vn_instance():
    global _vn
    if _vn is None:
        _vn = get_vanna()
    return _vn

def train_with_information_schema(limit_tables: Optional[List[str]] = None) -> Dict[str, Any]:
    vn = _vn_instance()
    df = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
    plan = vn.get_training_plan_generic(df)
    if limit_tables:
        plan = [p for p in plan if any(t.lower() in str(p).lower() for t in limit_tables)]
    vn.train(plan=plan)
    return {"trained": True, "steps": len(plan)}

def train_additional(ddl: str = "", documentation: str = "", sql: str = "") -> Dict[str, Any]:
    vn = _vn_instance()
    if ddl:
        vn.train(ddl=ddl)
    if documentation:
        vn.train(documentation=documentation)
    if sql:
        vn.train(sql=sql)
    return {"ok": True}

def ask(question: str, enforce_schema: str = "assistente") -> Dict[str, Any]:
    vn = _vn_instance()
    sql = vn.generate_sql(question=question)
    ok, reason = validate_sql(sql, allowed_schema=enforce_schema)
    if not ok:
        return {"error": f"Consulta bloqueada pelos guardrails: {reason}", "sql": sql}
    result = vn.run_sql(sql)
    return {"sql": sql, "result": result, "source": enforce_schema}
