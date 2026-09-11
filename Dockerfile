FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

# `.[stt-oss]`, not `.` — the bare install omits faster-whisper, which is the
# only STT provider that works without a Mistral key. A container that
# cannot transcribe unless you hold an API key is not the fallback the
# README describes.
RUN pip install --no-cache-dir '.[stt-oss]'

EXPOSE 8090

CMD ["lavoix-server"]
