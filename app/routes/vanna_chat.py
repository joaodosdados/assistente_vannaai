from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.nlq_vanna import ask, train_with_information_schema, train_additional

router = APIRouter(prefix="/vanna", tags=["vanna"])

class AskIn(BaseModel):
    question: str

class TrainSchemaIn(BaseModel):
    tables: list[str] | None = None

class TrainExtraIn(BaseModel):
    ddl: str = ""
    documentation: str = ""
    sql: str = ""

@router.post("/ask")
def vanna_ask(payload: AskIn):
    out = ask(payload.question)
    if "error" in out:
        raise HTTPException(status_code=400, detail=out)
    return out

@router.post("/train/schema")
def vanna_train_schema(payload: TrainSchemaIn):
    return train_with_information_schema(limit_tables=payload.tables)

@router.post("/train/extra")
def vanna_train_extra(payload: TrainExtraIn):
    return train_additional(ddl=payload.ddl, documentation=payload.documentation, sql=payload.sql)
