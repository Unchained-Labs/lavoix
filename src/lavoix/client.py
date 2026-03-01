from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx


class LavoixClient:
    def __init__(
        self, base_url: str = "http://localhost:8090", timeout_seconds: float = 120.0
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds

    def healthz(self) -> dict[str, Any]:
        response = httpx.get(f"{self._base_url}/healthz", timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def transcribe(
        self,
        audio_path: str | Path,
        language: str | None = None,
        provider: str | None = None,
    ) -> dict[str, Any]:
        path = Path(audio_path)
        data: dict[str, Any] = {}
        if language:
            data["language"] = language
        if provider:
            data["provider"] = provider

        with path.open("rb") as f:
            files = {"file": (path.name, f, "application/octet-stream")}
            response = httpx.post(
                f"{self._base_url}/v1/stt/transcribe",
                data=data,
                files=files,
                timeout=self._timeout,
            )
        response.raise_for_status()
        return response.json()

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        voice: str = "default",
        speed: float = 1.0,
        provider: str | None = None,
    ) -> Path:
        payload: dict[str, Any] = {
            "text": text,
            "voice": voice,
            "speed": speed,
            "provider": provider,
        }
        response = httpx.post(
            f"{self._base_url}/v1/tts/synthesize", json=payload, timeout=self._timeout
        )
        response.raise_for_status()

        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(response.content)
        return destination
