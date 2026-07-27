import pytest

from lavoix.config import Settings
from lavoix.schemas import TranscriptionResult
from lavoix.service import AudioService, UnknownProviderError


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


def test_tts_falls_back_to_oss_when_mistral_unconfigured():
    """`LAVOIX_DEFAULT_TTS_PROVIDER=mistral` without an API key should degrade to
    the local engine, not raise — matching the long-standing STT fallback."""
    settings = Settings(default_tts_provider="mistral", mistral_api_key=None)
    service = AudioService.from_settings(settings)

    assert "mistral" not in service.tts_providers
    assert service._pick_tts_provider(None) is service.tts_providers["oss"]


def test_reported_tts_provider_name_is_selectable():
    """The name echoed on X-Lavoix-Provider must be a valid `provider` value."""
    service = AudioService.from_settings(Settings(mistral_api_key=None))
    reported = service.tts_providers["oss"].name

    assert reported in service.tts_providers
    assert service._pick_tts_provider(reported) is service._pick_tts_provider("oss")


def test_unknown_provider_raises_unknown_provider_error():
    service = AudioService.from_settings(Settings(mistral_api_key=None))
    with pytest.raises(UnknownProviderError):
        service._pick_stt_provider("nope")
    with pytest.raises(UnknownProviderError):
        service._pick_tts_provider("nope")
