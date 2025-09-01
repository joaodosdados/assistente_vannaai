# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers do Vanna + UI (adicionados pelo pacote da branch)
from app.routes.vanna_chat import router as vanna_router
from app.ui.chat_router import router as chat_router
from app.playground_mount import mount_vanna_playground
from vanna.pgvector import PG_VectorStore

app = FastAPI(
    title="Assistente VANNAAI",
    version="0.2.0",
    description="MVP com UI de treinamento (Vanna + Postgres + Guardrails).",
)

mount_vanna_playground(app, prefix="/playground")

# CORS básico (ajuste conforme necessidade)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(vanna_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "ok": True,
        "app": "assistente-vannaai",
        "ui": "/admin/treinamento",
        "docs": "/docs",
    }


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}
