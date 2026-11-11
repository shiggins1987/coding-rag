import os
from pathlib import Path
from collections.abc import Mapping

import yaml
from pydantic import BaseModel

_OVERRIDES = {
    "CODING_RAG_MARKER_URL": ("marker", "url"),
    "CODING_RAG_EMBEDDINGS_URL": ("embeddings", "url"),
    "CODING_RAG_EMBEDDINGS_MODEL": ("embeddings", "model"),
    "CODING_RAG_EMBEDDINGS_API_KEY": ("embeddings", "api_key"),
    "CODING_RAG_CHAT_URL": ("chat", "url"),
    "CODING_RAG_CHAT_MODEL": ("chat", "model"),
    "CODING_RAG_CHAT_API_KEY": ("chat", "api_key"),
    "CODING_RAG_QDRANT_URL": ("qdrant", "url"),
}

class Endpoint(BaseModel):
    url: str
    model: str | None = None
    api_key: str | None = None

class Settings(BaseModel):
    marker: Endpoint = Endpoint(url="http://127.0.0.1:8001")
    embeddings: Endpoint = Endpoint(
        url="http://127.0.0.1:11434", model="nomic-embed-text"
    )
    chat: Endpoint = Endpoint(url="http://127.0.0.1:11434", model="qwen3:8b")
    qdrant: Endpoint = Endpoint(url="http://127.0.0.1:6333")

def load_config(path: Path, env: Mapping[str, str] | None = None) -> Settings:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    env = os.environ if env is None else env
    for key, (section, field) in _OVERRIDES.items():
        if env.get(key):
            raw.setdefault(section, {})[field] = env[key]
    return Settings.model_validate(raw)
