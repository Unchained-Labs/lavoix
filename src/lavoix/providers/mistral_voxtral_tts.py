from __future__ import annotations

import httpx

from .base import TtsProvider


class MistralVoxtralTtsProvider(TtsProvider):
    name = "mistral"

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def synthesize(self, text: str, voice: str, speed: float) -> tuple[bytes, str]:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        payload = {
            "model": self._model,
            "input": text,
            "voice": voice,
            "speed": speed,
            "format": "wav",
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/audio/speech", headers=headers, json=payload
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "audio/wav")
            return response.content, content_type
