# REST API Reference

Base URL: `http://localhost:8090`

## Health

### `GET /healthz`

Response:

```json
{"status":"ok"}
```

## Speech-to-Text

### `POST /v1/stt/transcribe`

Content type: `multipart/form-data`

Fields:

- `file` (required): audio file
- `language` (optional)
- `provider` (optional)

Success response: transcription payload (`TranscriptionResult`-compatible JSON).

Failure responses:

- `400` for empty file
- `500` for provider/runtime failures

## Text-to-Speech

### `POST /v1/tts/synthesize`

Content type: `application/json`

Body:

```json
{
  "text": "hello",
  "voice": "default",
  "speed": 1.0,
  "provider": "mistral"
}
```

Success response:

- binary audio body
- `Content-Type` = provider-selected media type
- `X-Lavoix-Provider` header

Failure response:

- `500` with error detail
