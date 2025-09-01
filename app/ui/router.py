# app/ui/router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

from app.services.nlq_vanna import train_with_information_schema, train_additional, ask

router = APIRouter(prefix="/admin", tags=["ui-admin"])
templates = Jinja2Templates(directory="app/ui/templates")

@router.get("/treinamento", response_class=HTMLResponse)
def treinamento_page(request: Request):
    return templates.TemplateResponse("treinamento.html", {"request": request})

@router.post("/treinar/schema", response_class=HTMLResponse)
def treinar_schema(request: Request, tables: str = Form(default="")):
    tlist = [t.strip() for t in tables.split(",") if t.strip()] if tables else None
    res = train_with_information_schema(limit_tables=tlist)
    return templates.TemplateResponse("partials/response.html", {"request": request, "payload": json.dumps(res, ensure_ascii=False, indent=2)})

@router.post("/treinar/extra", response_class=HTMLResponse)
def treinar_extra(request: Request, ddl: str = Form(default=""), documentation: str = Form(default=""), sql: str = Form(default="")):
    res = train_additional(ddl=ddl, documentation=documentation, sql=sql)
    return templates.TemplateResponse("partials/response.html", {"request": request, "payload": json.dumps(res, ensure_ascii=False, indent=2)})

@router.post("/perguntar", response_class=HTMLResponse)
def perguntar(request: Request, question: str = Form(...)):
    res = ask(question)
    return templates.TemplateResponse("partials/response.html", {"request": request, "payload": json.dumps(res, ensure_ascii=False, indent=2)})
