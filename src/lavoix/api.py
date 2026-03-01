from __future__ import annotations

import logging

import uvicorn
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from lavoix.config import Settings
from lavoix.schemas import SynthesisRequest
from lavoix.service import AudioService

logger = logging.getLogger("lavoix.api")


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()
    service = AudioService.from_settings(app_settings)
    app = FastAPI(title="lavoix", version="0.1.0")
    app.state.audio_service = service

    def get_service() -> AudioService:
        return app.state.audio_service

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/stt/transcribe")
    async def transcribe(
        file: UploadFile = File(...),
        language: str | None = Form(default=None),
        provider: str | None = Form(default=None),
        audio_service: AudioService = Depends(get_service),
    ):
        try:
            audio = await file.read()
            if not audio:
                raise HTTPException(status_code=400, detail="Empty audio file.")
            result = await audio_service.transcribe(
                audio_bytes=audio,
                filename=file.filename or "audio.wav",
                content_type=file.content_type,
                language=language,
                provider=provider,
            )
            return result
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Transcription failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.post("/v1/tts/synthesize")
    async def synthesize(
        payload: SynthesisRequest, audio_service: AudioService = Depends(get_service)
    ):
        try:
            metadata, audio = await audio_service.synthesize(
                text=payload.text,
                voice=payload.voice,
                speed=payload.speed,
                provider=payload.provider,
            )
            headers = {"X-Lavoix-Provider": metadata.provider}
            return Response(content=audio, media_type=metadata.content_type, headers=headers)
        except Exception as exc:
            logger.exception("Synthesis failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return app


def run() -> None:
    settings = Settings()
    uvicorn.run(
        "lavoix.api:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        log_level="info",
    )
