from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.ports import Ready


class AlwaysReady:
    def ready(self) -> bool:
        return True


def create_app(
    marker: Ready | None = None,
    embeddings: Ready | None = None,
    chat: Ready | None = None,
    vector_store: Ready | None = None,
) -> FastAPI:
    app = FastAPI()
    app.state.marker = marker or AlwaysReady()
    app.state.embeddings = embeddings or AlwaysReady()
    app.state.chat = chat or AlwaysReady()
    app.state.vector_store = vector_store or AlwaysReady()

    @app.get("/health")
    def health(request: Request):
        state = request.app.state
        checks = {
            "marker": state.marker.ready(),
            "embeddings": state.embeddings.ready(),
            "chat": state.chat.ready(),
            "vector_store": state.vector_store.ready(),
        }
        ok = all(checks.values())
        return JSONResponse(
            status_code=200 if ok else 503,
            content={"status": "ok" if ok else "degraded", "checks": checks},
        )
    return app
