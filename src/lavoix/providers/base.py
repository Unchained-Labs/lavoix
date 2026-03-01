from __future__ import annotations

from abc import ABC, abstractmethod

from lavoix.schemas import TranscriptionResult


class SttProvider(ABC):
    name: str

    @abstractmethod
    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str | None = None,
        language: str | None = None,
    ) -> TranscriptionResult:
        raise NotImplementedError


class TtsProvider(ABC):
    name: str

    @abstractmethod
    async def synthesize(self, text: str, voice: str, speed: float) -> tuple[bytes, str]:
        """
        Returns a tuple of (audio_bytes, content_type).
        """
        raise NotImplementedError
