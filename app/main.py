# app/main.py (trecho relevante)
from fastapi import FastAPI
from .routers import status, nlq, chat
from .services.vanna_client import build_vanna, connect_and_seed


app = FastAPI(title="Assistente de processos MVP")
app.include_router(status.router)
app.include_router(nlq.router)
app.include_router(chat.router)

_vn = None


@app.on_event("startup")
def _startup():
    global _vn
    _vn = build_vanna()
    connect_and_seed(_vn)
    # 👇 disponibiliza para os routers sem import circular
    app.state.vanna = _vn


@app.get("/health")
def health():
    return {"status": "ok"}
