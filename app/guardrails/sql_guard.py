# app/guardrails/sql_guard.py
import re
from typing import Tuple

DDL_DML = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|COPY)\b", re.IGNORECASE)
MULTI_STMT = re.compile(r";\s*\S", re.DOTALL)
DISALLOWED_FUNCS = re.compile(r"\b(pg_|pg_catalog|information_schema)\b", re.IGNORECASE)

def validate_sql(sql: str, allowed_schema: str = "assistente") -> Tuple[bool, str]:
    s = sql.strip()
    if not (s.lower().startswith("select") or s.lower().startswith("with")):
        return False, "Somente SELECT/CTE é permitido"
    if DDL_DML.search(s):
        return False, "DDL/DML proibidos"
    if MULTI_STMT.search(s):
        return False, "Múltiplos statements proibidos"
    explicit_schemas = re.findall(r"([a-zA-Z_][\w]*)\.", s)
    for sch in explicit_schemas:
        if sch.lower() != allowed_schema.lower():
            return False, f"Schema não permitido: {sch}"
    if DISALLOWED_FUNCS.search(s):
        return False, "Funções/catálogos não permitidos"
    return True, "ok"
