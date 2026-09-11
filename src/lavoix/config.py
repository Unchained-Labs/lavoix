from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LAVOIX_", extra="ignore")

    app_name: str = "lavoix"
    host: str = "0.0.0.0"
    port: int = 8090

    mistral_api_key: str | None = Field(default=None)
    mistral_base_url: str = "https://api.mistral.ai/v1"
    voxtral_model: str = "voxtral-mini-latest"
    voxtral_tts_model: str = "voxtral-tts-latest"

    #: Which faster-whisper model the local provider loads.
    #:
    #: Was hardcoded to "small", which is a fine default on a laptop and a bad
    #: one on a small always-on box: the model is resident for the life of the
    #: process, and "small" is roughly a gigabyte of it. Exposed so a deployment
    #: can trade accuracy for memory without patching the provider — "base" and
    #: "tiny" are the useful steps down.
    whisper_model: str = "small"
    #: "cpu", "cuda", or "auto". Left as cpu by default because a box that has a
    #: GPU knows it and a box that does not should not fail at import time.
    whisper_device: str = "cpu"
    #: int8 on CPU is roughly half the memory of float32 for a small accuracy
    #: cost — the right trade anywhere the model is not the point of the machine.
    whisper_compute_type: str = "int8"

    default_stt_provider: str = "mistral"
    default_tts_provider: str = "oss"
