from __future__ import annotations

from dataclasses import dataclass

from lavoix.config import Settings
from lavoix.schemas import SynthesisResult, TranscriptionResult

from .providers.base import SttProvider, TtsProvider
from .providers.faster_whisper_stt import FasterWhisperSttProvider
from .providers.mistral_voxtral import MistralVoxtralSttProvider
from .providers.mistral_voxtral_tts import MistralVoxtralTtsProvider
from .providers.pyttsx3_tts import Pyttsx3TtsProvider


@dataclass
class AudioService:
    settings: Settings
    stt_providers: dict[str, SttProvider]
    tts_providers: dict[str, TtsProvider]

    @classmethod
    def from_settings(cls, settings: Settings) -> AudioService:
        stt_providers: dict[str, SttProvider] = {"faster-whisper": FasterWhisperSttProvider()}
        tts_providers: dict[str, TtsProvider] = {"oss": Pyttsx3TtsProvider()}

        if settings.mistral_api_key:
            stt_providers["mistral"] = MistralVoxtralSttProvider(
                api_key=settings.mistral_api_key,
                base_url=settings.mistral_base_url,
                model=settings.voxtral_model,
            )
            tts_providers["mistral"] = MistralVoxtralTtsProvider(
                api_key=settings.mistral_api_key,
                base_url=settings.mistral_base_url,
                model=settings.voxtral_tts_model,
            )

        return cls(settings=settings, stt_providers=stt_providers, tts_providers=tts_providers)

    def _pick_stt_provider(self, requested: str | None) -> SttProvider:
        key = requested or self.settings.default_stt_provider
        provider = self.stt_providers.get(key)
        if provider is not None:
            return provider
        if key == "mistral" and "faster-whisper" in self.stt_providers:
            return self.stt_providers["faster-whisper"]
        available = ", ".join(sorted(self.stt_providers))
        raise ValueError(f"Unknown STT provider '{key}'. Available: {available}")

    def _pick_tts_provider(self, requested: str | None) -> TtsProvider:
        key = requested or self.settings.default_tts_provider
        provider = self.tts_providers.get(key)
        if provider is not None:
            return provider
        available = ", ".join(sorted(self.tts_providers))
        raise ValueError(f"Unknown TTS provider '{key}'. Available: {available}")

    async def transcribe(
        self,
        audio_bytes: bytes,
        filename: str,
        content_type: str | None = None,
        language: str | None = None,
        provider: str | None = None,
    ) -> TranscriptionResult:
        stt_provider = self._pick_stt_provider(provider)
        return await stt_provider.transcribe(
            audio_bytes=audio_bytes,
            filename=filename,
            content_type=content_type,
            language=language,
        )

    async def synthesize(
        self,
        text: str,
        voice: str = "default",
        speed: float = 1.0,
        provider: str | None = None,
    ) -> tuple[SynthesisResult, bytes]:
        tts_provider = self._pick_tts_provider(provider)
        audio, content_type = await tts_provider.synthesize(text=text, voice=voice, speed=speed)
        return SynthesisResult(provider=tts_provider.name, content_type=content_type), audio
