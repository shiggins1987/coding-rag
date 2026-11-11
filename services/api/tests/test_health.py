from fastapi.testclient import TestClient

from app.main import create_app
from tests.fakes import FakeReady


def test_health_is_ready_when_port_is_up():
    app = create_app(
        marker=FakeReady(),
        embeddings=FakeReady(),
        chat=FakeReady(),
        vector_store=FakeReady(),
    )
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": {
            "marker": True,
            "embeddings": True,
            "chat": True,
            "vector_store": True,
        },
    }


def test_health_is_degraded_when_a_port_is_down():
    app = create_app(
        marker=FakeReady(ok=False),
        embeddings=FakeReady(),
        chat=FakeReady(),
        vector_store=FakeReady(),
    )
    response = TestClient(app).get("/health")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["checks"]["marker"] is False
    assert body["checks"]["chat"] is True
