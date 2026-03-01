from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from lavoix.schemas import TranscriptionResult

from .base import SttProvider


class FasterWhisperSttProvider(SttProvider):
    name = "faster-whisper"

    def __init__(self, model: str = "small") -> None:
        self._model_name = model
        self._model = None

    def _ensure_model(self):
        if self._model is not None:
            return self._model
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:  # pragma: no cover - depends on optional extras
            raise RuntimeError(
                "faster-whisper is not installed. Install with `pip install lavoix[stt-oss]`."
            ) from exc
        self._model = WhisperModel(self._model_name)
        return self._model

    def _transcribe_blocking(self, file_path: Path, language: str | None) -> TranscriptionResult:
        model = self._ensure_model()
        segments, info = model.transcribe(str(file_path), language=language)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return TranscriptionResult(
            text=text,
            model=self._model_name,
            provider=self.name,
            language=info.language if info else language,
            raw={"duration": getattr(info, "duration", None)},
        )

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str | None = None,
        language: str | None = None,
    ) -> TranscriptionResult:
        suffix = Path(filename).suffix or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = Path(tmp.name)
        try:
            return await asyncio.to_thread(self._transcribe_blocking, tmp_path, language)
        finally:
            tmp_path.unlink(missing_ok=True)
