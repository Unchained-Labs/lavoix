# API Overview

lavoix exposes two API surfaces:

- **REST service API** for networked integration.
- **Python library API** for in-process usage.

## REST surface

Primary endpoints:

- `GET /healthz`
- `POST /v1/stt/transcribe`
- `POST /v1/tts/synthesize`

See [REST API](/api/rest-api).

## Python surface

Primary client:

- `LavoixClient`

Key methods:

- `healthz()`
- `transcribe(audio_path, language=None, provider=None)`
- `synthesize(text, output_path, voice="default", speed=1.0, provider=None)`

See [Library API](/api/library-api).
