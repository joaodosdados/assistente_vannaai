from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.routes.vanna_chat import router as vanna_router
except ModuleNotFoundError:
    # fallback if app isn't a package on PYTHONPATH
    from .routes.vanna_chat import router as vanna_router  # type: ignore

try:
    from app.ui.router import router as ui_router
except ModuleNotFoundError:
    from .ui.router import router as ui_router  # type: ignore

app = FastAPI(title="Assistente VANNAAI", version="0.2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vanna_router)
app.include_router(ui_router)

@app.get("/")
def root():
    return {"ok": True, "ui": "/admin/treinamento", "docs": "/docs"}
