import re

ALLOWLIST_VIEWS = {"assistente.vw_processo", "assistente.vw_evento_processo"}


def is_sql_safe(sql: str) -> bool:
    s = f" {sql.strip().lower()} "
    banned = [
        " delete ",
        " update ",
        " insert ",
        " drop ",
        " alter ",
        " copy ",
        ";",
        "--",
        "/*",
        "*/",
    ]
    if any(k in s for k in banned):
        return False
    if "select *" in s:
        return False
    if not any(v.lower() in s for v in ALLOWLIST_VIEWS):
        return False
    if s.count(" join ") > 2:
        return False
    return True


def enforce_limit(sql: str, max_rows: int = 200) -> str:
    return (
        sql
        if re.search(r"\blimit\b", sql, re.I)
        else f"{sql.rstrip()}\nLIMIT {max_rows}"
    )


def coerce_types(sql: str) -> str:
    # id_processo é VARCHAR -> força literal com aspas
    sql = re.sub(
        r"(id_processo\s*=\s*)(\d+)(\b)", r"\1'\2'\3", sql, flags=re.IGNORECASE
    )
    return sql
