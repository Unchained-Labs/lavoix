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


def test_healthz_reports_available_providers():
    app = create_app(Settings(mistral_api_key=None))
    client = TestClient(app)
    response = client.get("/healthz")

    assert response.status_code == 200
    body = response.json()
    assert "oss" in body["providers"]["tts"]
    assert body["defaults"]["stt"]


def test_unknown_provider_is_client_error_not_server_error():
    app = create_app(Settings(mistral_api_key=None))
    client = TestClient(app)
    response = client.post(
        "/v1/stt/transcribe",
        files={"file": ("a.wav", b"audio-bytes", "audio/wav")},
        data={"provider": "does-not-exist"},
    )
    assert response.status_code == 400
