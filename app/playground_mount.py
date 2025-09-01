from typing import Optional
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles
import pkgutil, pathlib, sys

from app.vanna_integration import get_vanna


def _as_wsgi(obj):
    """Return a WSGI callable from a VannaFlaskApp instance or Flask app.

    Known possibilities across versions:
      - obj (callable Flask app)
      - obj.app
      - obj.flask
      - obj.flask_app   <-- most common in docs
      - obj.wsgi_app
    """
    # If it's already a Flask app (Flask is callable)
    if callable(obj):
        return obj

    for attr in ("flask_app", "app", "flask", "wsgi_app"):
        if hasattr(obj, attr):
            inner = getattr(obj, attr)
            if callable(inner):
                return inner

    raise TypeError(
        "Could not obtain a WSGI callable from VannaFlaskApp (checked: flask_app, app, flask, wsgi_app)"
    )


class _LazyWSGIApp:
    def __init__(self):
        self._wsgi: Optional[WSGIMiddleware] = None
        self._error: Optional[str] = None

    def _ensure(self):
        if self._wsgi is None and self._error is None:
            try:
                from vanna.flask import VannaFlaskApp

                vn = get_vanna()  # build only on first access
                vanna_flask = VannaFlaskApp(vn)
                wsgi = _as_wsgi(vanna_flask)
                self._wsgi = WSGIMiddleware(wsgi)
            except Exception as e:
                self._error = f"Playground init failed: {e}"

    async def __call__(self, scope, receive, send):
        if self._wsgi is None:
            self._ensure()
        if self._wsgi is None:
            resp = PlainTextResponse(
                self._error or "Playground failed to initialize", status_code=500
            )
            await resp(scope, receive, send)
            return
        await self._wsgi(scope, receive, send)


def _resolve_wsgi(app_obj):
    for attr in ("flask_app", "app", "flask", "wsgi_app"):
        if hasattr(app_obj, attr) and callable(getattr(app_obj, attr)):
            return getattr(app_obj, attr)
    if callable(app_obj):
        return app_obj
    raise TypeError(
        "Não consegui obter o WSGI callable de VannaFlaskApp (tentei flask_app, app, flask, wsgi_app)."
    )


def _resolve_assets_dir() -> Optional[str]:
    """Tenta localizar diretórios com os assets do playground dentro do pacote vanna.flask."""
    loader = pkgutil.get_loader("vanna.flask")
    if not loader:
        print("[playground] pacote vanna.flask não encontrado", file=sys.stderr)
        return None
    base = pathlib.Path(loader.get_filename()).parent  # .../site-packages/vanna/flask
    candidates = [
        base / "static" / "assets",
        base / "static",
        base / "assets",
        base,
    ]
    # preferimos onde existam arquivos index-*.js/css
    for c in candidates:
        if c.is_dir():
            has_js = any(
                p.name.startswith("index-") and p.suffix == ".js"
                for p in c.glob("index-*.js")
            )
            has_css = any(
                p.name.startswith("index-") and p.suffix == ".css"
                for p in c.glob("index-*.css")
            )
            if has_js or has_css:
                print(f"[playground] assets encontrados em: {c}")
                return str(c)

    # busca profunda por index-*.js
    for p in base.rglob("index-*.js"):
        print(f"[playground] assets (deep) em: {p.parent}")
        return str(p.parent)

    print(
        "[playground] nenhum index-*.js|css encontrado dentro de vanna.flask",
        file=sys.stderr,
    )
    return None


def mount_vanna_playground(app: FastAPI, prefix: str = "/playground"):
    # 1) Monta o webapp Flask do Vanna
    try:
        from vanna.flask import VannaFlaskApp

        vn = get_vanna()
        vf = VannaFlaskApp(vn)
        wsgi = _resolve_wsgi(vf)
        app.mount(prefix, WSGIMiddleware(wsgi))
        print("[playground] Flask montado em", prefix)
    except Exception as e:
        app.mount(
            prefix, PlainTextResponse(f"Playground init failed: {e}", status_code=500)
        )
        print(f"[playground] falha ao montar Flask: {e}", file=sys.stderr)

    # 2) Monta /assets a partir do diretório detectado
    assets_dir = _resolve_assets_dir()
    if assets_dir:
        app.mount("/assets", StaticFiles(directory=assets_dir), name="vanna-assets")
        print("[playground] /assets montado em:", assets_dir)
    else:
        print(
            "[playground] aviso: /assets NÃO montado (assets ausentes no pacote)",
            file=sys.stderr,
        )
