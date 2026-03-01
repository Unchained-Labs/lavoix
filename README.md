# lavoix

[![CI](https://github.com/Unchained-Labs/lavoix/actions/workflows/ci.yml/badge.svg)](https://github.com/Unchained-Labs/lavoix/actions/workflows/ci.yml)

`lavoix` is a Python library + FastAPI server for speech workflows:

- **Speech-to-Text (STT):** Voxtral-first via Mistral API
- **Text-to-Speech (TTS):** Voxtral TTS path via Mistral API + OSS fallback (`pyttsx3`)
- **Production shape:** clean provider abstraction, typed config, HTTP API, and Python client

## Why this architecture

- Voxtral is used as the primary STT path (best quality for Mistral-native workflows).
- TTS is implemented with an OSS provider so you can run locally/offline.
- The service is provider-driven, so adding more engines (e.g. a future Mistral TTS endpoint) is straightforward.

## Quick Start

### 1) Install

```bash
cd /home/wardn/dev/mistral-dev/lavoix
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts-oss]"
```

Optional local STT fallback:

```bash
pip install -e ".[stt-oss]"
```

### 2) Configure env

Create `.env`:

```env
LAVOIX_MISTRAL_API_KEY=your_key_here
LAVOIX_VOXTRAL_MODEL=voxtral-mini-latest
LAVOIX_DEFAULT_STT_PROVIDER=mistral
LAVOIX_VOXTRAL_TTS_MODEL=voxtral-tts-latest
LAVOIX_DEFAULT_TTS_PROVIDER=mistral
LAVOIX_PORT=8090
```

### 3) Run server

```bash
lavoix-server
```

### 4) Use API

Health:

```bash
curl http://localhost:8090/healthz
```

Transcription:

```bash
curl -X POST http://localhost:8090/v1/stt/transcribe \
  -F "file=@./sample.wav" \
  -F "provider=mistral"
```

Synthesis:

```bash
curl -X POST http://localhost:8090/v1/tts/synthesize \
  -H "content-type: application/json" \
  -d '{"text":"Hello from lavoix","voice":"default","speed":1.0}' \
  --output out.wav
```

## Python Client

```python
from lavoix import LavoixClient

client = LavoixClient("http://localhost:8090")
print(client.healthz())

stt = client.transcribe("sample.wav", provider="mistral")
print(stt["text"])

client.synthesize("Bonjour Erwin", "out.wav")
```

## Endpoints

- `GET /healthz`
- `POST /v1/stt/transcribe` (multipart form: `file`, optional `language`, optional `provider`)
- `POST /v1/tts/synthesize` (JSON body: `text`, `voice`, `speed`, optional `provider`)

## Integration With Otter/Seal

- Otter forwards voice prompts to Lavoix for transcription.
- Seal consumes that flow through Otter (`POST /v1/voice/prompts`) and keeps voice-first task creation.
- Lavoix can also be used standalone as a generic STT/TTS service.

## Quality Gates

- Pre-commit config is included in `.pre-commit-config.yaml`.
- GitHub Actions CI runs lint/format checks and tests on push/PR.

Enable hooks locally:

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

## Notes

- If Mistral API key is missing, `mistral` STT/TTS providers are unavailable; use `faster-whisper` for STT and `oss` for TTS.
- `pyttsx3` may require system speech backends (like `espeak`) depending on OS.
