from pydantic import BaseModel, Field


class TranscriptionResult(BaseModel):
    text: str
    model: str | None = None
    provider: str
    language: str | None = None
    raw: dict | None = None


class SynthesisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    voice: str = "default"
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    provider: str | None = None


class SynthesisResult(BaseModel):
    provider: str
    content_type: str = "audio/wav"
    sample_rate: int | None = None
