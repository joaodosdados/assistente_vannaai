# app/ui/chat_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json

from app.services.nlq_vanna import ask

router = APIRouter(prefix="/chat", tags=["chat-ui"])
templates = Jinja2Templates(directory="app/ui/templates")


@router.get("", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/send", response_class=HTMLResponse)
def chat_send(request: Request, message: str = Form(...)):
    result = ask(message)
    payload = {
        "question": message,
        "sql": result.get("sql"),
        "result": result.get("result"),
        "error": result.get("error"),
        "ts": datetime.utcnow().isoformat(),
    }
    return templates.TemplateResponse(
        "partials/chat_message.html",
        {
            "request": request,
            "payload": json.dumps(payload, ensure_ascii=False, indent=2),
        },
    )
