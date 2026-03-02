# Library API Reference

## `LavoixClient`

Defined in `src/lavoix/client.py`.

### Constructor

```python
LavoixClient(base_url: str = "http://localhost:8090", timeout_seconds: float = 120.0)
```

### `healthz() -> dict[str, Any]`

Checks service health and returns parsed JSON response.

### `transcribe(audio_path, language=None, provider=None) -> dict[str, Any]`

Uploads a local audio file and returns transcription payload.

Parameters:

- `audio_path`: file path
- `language`: optional hint
- `provider`: optional provider override

### `synthesize(text, output_path, voice="default", speed=1.0, provider=None) -> Path`

Sends synthesis request and writes output audio to disk.

Parameters:

- `text`: input text
- `output_path`: destination path
- `voice`: voice profile
- `speed`: playback speed multiplier
- `provider`: optional provider override

## Error behavior

- HTTP non-success statuses raise via `response.raise_for_status()`.
- File write path is created if missing parent directories do not exist.
