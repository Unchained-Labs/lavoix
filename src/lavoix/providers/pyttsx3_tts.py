from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from .base import TtsProvider


class Pyttsx3TtsProvider(TtsProvider):
    name = "pyttsx3"

    def _synthesize_blocking(self, text: str, voice: str, speed: float) -> bytes:
        try:
            import pyttsx3
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "pyttsx3 is not installed. Install with `pip install lavoix[tts-oss]`."
            ) from exc

        engine = pyttsx3.init()
        engine.setProperty("rate", int(200 * speed))
        if voice and voice != "default":
            for v in engine.getProperty("voices"):
                if voice.lower() in (v.id or "").lower() or voice.lower() in (v.name or "").lower():
                    engine.setProperty("voice", v.id)
                    break

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = Path(tmp.name)
        try:
            engine.save_to_file(text, str(output_path))
            engine.runAndWait()
            return output_path.read_bytes()
        finally:
            output_path.unlink(missing_ok=True)

    async def synthesize(self, text: str, voice: str, speed: float) -> tuple[bytes, str]:
        audio = await asyncio.to_thread(self._synthesize_blocking, text, voice, speed)
        return audio, "audio/wav"
