# Tutorial: Building a Custom Provider

This guide explains how to add a new STT or TTS provider to lavoix.

## 1. Implement provider interface

Create a new file under `src/lavoix/providers/`.

- For STT, implement `SttProvider`.
- For TTS, implement `TtsProvider`.

Example shape:

```python
class MySttProvider(SttProvider):
    name = "my-provider"

    async def transcribe(self, audio_bytes, filename, content_type=None, language=None):
        ...
```

## 2. Return normalized payloads

Your implementation should produce outputs compatible with lavoix schemas rather than provider-specific raw responses.

## 3. Register in service/provider resolution

Wire your provider into the selection map used by `AudioService.from_settings(...)`.

## 4. Add configuration surface

If the provider requires new credentials or model identifiers:

- extend `Settings` in `src/lavoix/config.py`
- document new `LAVOIX_*` variables

## 5. Add tests

At minimum include:

- successful transcription/synthesis path
- failure behavior normalization
- provider selection behavior

## 6. Validate through API

Use the same REST endpoints with `provider=<your-provider>` to verify integration behavior without changing upstream clients.
