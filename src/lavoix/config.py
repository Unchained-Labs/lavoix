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

    default_stt_provider: str = "mistral"
    default_tts_provider: str = "oss"
