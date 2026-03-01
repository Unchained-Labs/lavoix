from __future__ import annotations

from typing import Any

import httpx

from lavoix.schemas import TranscriptionResult

from .base import SttProvider


class MistralVoxtralSttProvider(SttProvider):
    name = "mistral"

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str | None = None,
        language: str | None = None,
    ) -> TranscriptionResult:
        files = {
            "file": (filename, audio_bytes, content_type or "application/octet-stream"),
        }
        data: dict[str, Any] = {"model": self._model}
        if language:
            data["language"] = language

        headers = {"Authorization": f"Bearer {self._api_key}"}

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/audio/transcriptions",
                headers=headers,
                data=data,
                files=files,
            )
            response.raise_for_status()
            payload = response.json()

        text = str(payload.get("text") or payload.get("transcript") or "").strip()
        if not text:
            raise ValueError("Mistral transcription returned an empty transcript.")

        return TranscriptionResult(
            text=text,
            model=self._model,
            provider=self.name,
            language=language,
            raw=payload,
        )
