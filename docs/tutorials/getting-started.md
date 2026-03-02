# Tutorial: Getting Started

This tutorial sets up lavoix for local development and validates STT/TTS end to end.

## 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts-oss]"
```

Optional STT fallback:

```bash
pip install -e ".[stt-oss]"
```

## 2. Configure environment

Create `.env`:

```env
LAVOIX_MISTRAL_API_KEY=your_key_here
LAVOIX_VOXTRAL_MODEL=voxtral-mini-latest
LAVOIX_DEFAULT_STT_PROVIDER=mistral
LAVOIX_VOXTRAL_TTS_MODEL=voxtral-tts-latest
LAVOIX_DEFAULT_TTS_PROVIDER=mistral
LAVOIX_PORT=8090
```

## 3. Start the server

```bash
lavoix-server
```

## 4. Validate service health

```bash
curl http://localhost:8090/healthz
```

Expected response:

```json
{"status":"ok"}
```

## 5. Validate STT

```bash
curl -X POST http://localhost:8090/v1/stt/transcribe \
  -F "file=@./sample.wav" \
  -F "provider=mistral"
```

## 6. Validate TTS

```bash
curl -X POST http://localhost:8090/v1/tts/synthesize \
  -H "content-type: application/json" \
  -d '{"text":"hello from lavoix","voice":"default","speed":1.0}' \
  --output out.wav
```

## 7. Verify Python client

```python
from lavoix import LavoixClient

client = LavoixClient("http://localhost:8090")
print(client.healthz())
print(client.transcribe("sample.wav", provider="mistral"))
client.synthesize("hello", "out.wav")
```
