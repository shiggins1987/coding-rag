from pathlib import Path

from app.config import load_config

_YAML = """
marker: {url: http://from-file:8001}
embeddings: {url: http://embed:11434, model: nomic-embed-text}
chat: {url: http://chat:11434, model: qwen3:8b}
qdrant: {url: http://qdrant:6333}
"""


def test_env_overrides_url_and_file_keeps_model(tmp_path: Path):
    path = tmp_path / "config.yaml"
    path.write_text(_YAML)
    cfg = load_config(path, {"CODING_RAG_MARKER_URL": "http://from-env:9"})
    assert cfg.marker.url == "http://from-env:9"
    assert cfg.chat.model == "qwen3:8b"
    assert cfg.chat.api_key is None
