# Software Architecture

## Architectural Principles

lavoix is structured around three principles:

1. **Provider isolation**: each STT/TTS engine is implemented behind a strict abstract interface.
2. **Transport stability**: HTTP contracts remain consistent even when providers differ.
3. **Operational clarity**: failures are surfaced in predictable ways for orchestration and incident response.

## Runtime Components

- **API layer** (`src/lavoix/api.py`): FastAPI app exposing `/healthz`, `/v1/stt/transcribe`, `/v1/tts/synthesize`.
- **Service layer** (`src/lavoix/service.py`): orchestrates provider resolution and request execution.
- **Provider layer** (`src/lavoix/providers/*`): concrete Mistral and OSS engines.
- **Schema/config layer** (`src/lavoix/schemas.py`, `src/lavoix/config.py`): typed request and environment contracts.
- **Client layer** (`src/lavoix/client.py`): Python SDK for programmatic consumers.

## Provider Abstraction Model

`SttProvider` and `TtsProvider` define the execution contract:

- `SttProvider.transcribe(...) -> TranscriptionResult`
- `TtsProvider.synthesize(...) -> tuple[bytes, content_type]`

This design lets you add providers with minimal impact to callers.

## Request Lifecycle

### STT

1. Multipart upload arrives at `POST /v1/stt/transcribe`.
2. API validates request and reads bytes.
3. Service selects provider (request override or default).
4. Provider returns normalized transcription payload.
5. API returns JSON result.

### TTS

1. JSON payload arrives at `POST /v1/tts/synthesize`.
2. Service selects provider and synthesizes audio.
3. API responds with raw audio bytes and content type.
4. Header `X-Lavoix-Provider` identifies the provider used.

## Reliability and Failure Boundaries

- Empty audio uploads are rejected with `400`.
- Provider/runtime failures are normalized to `500` with diagnostic detail.
- Default provider selection is explicit and configurable through environment.

## Integration Position in the Kymatics Stack

- `seal` captures voice intent and delegates to `otter`.
- `otter` uses `lavoix` for speech transformation in voice workflows.
- `lavoix` can also operate as a standalone speech service.
