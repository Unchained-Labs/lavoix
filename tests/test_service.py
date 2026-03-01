import pytest

from lavoix.config import Settings
from lavoix.schemas import TranscriptionResult
from lavoix.service import AudioService


class DummySttProvider:
    name = "dummy"

    async def transcribe(self, audio_bytes, filename, content_type=None, language=None):
        return TranscriptionResult(
            text=f"ok:{filename}",
            model="dummy-model",
            provider=self.name,
            language=language,
        )


class DummyTtsProvider:
    name = "dummy-tts"

    async def synthesize(self, text, voice, speed):
        return f"{text}|{voice}|{speed}".encode(), "audio/wav"


@pytest.mark.asyncio
async def test_audio_service_provider_override():
    settings = Settings(default_stt_provider="dummy", default_tts_provider="dummy-tts")
    service = AudioService(
        settings=settings,
        stt_providers={"dummy": DummySttProvider()},
        tts_providers={"dummy-tts": DummyTtsProvider()},
    )

    stt = await service.transcribe(b"bytes", "sample.wav")
    assert stt.provider == "dummy"
    assert stt.text == "ok:sample.wav"

    metadata, audio = await service.synthesize("hello", provider="dummy-tts")
    assert metadata.provider == "dummy-tts"
    assert audio.startswith(b"hello")


@pytest.mark.asyncio
async def test_audio_service_unknown_provider():
    settings = Settings(default_stt_provider="missing")
    service = AudioService(settings=settings, stt_providers={}, tts_providers={})
    with pytest.raises(ValueError):
        await service.transcribe(b"bytes", "a.wav")
