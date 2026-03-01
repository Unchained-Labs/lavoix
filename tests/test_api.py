from fastapi.testclient import TestClient

from lavoix.api import create_app
from lavoix.config import Settings


def test_healthz():
    app = create_app(Settings())
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_transcribe_rejects_empty_file():
    app = create_app(Settings())
    client = TestClient(app)
    response = client.post(
        "/v1/stt/transcribe",
        files={"file": ("empty.wav", b"", "audio/wav")},
    )
    assert response.status_code == 400
