---
layout: home

hero:
  name: "lavoix"
  text: "Speech Infrastructure for Production Workflows"
  tagline: "Provider-driven STT/TTS library + service with stable contracts and operational clarity."
  actions:
    - theme: brand
      text: Get Started
      link: /tutorials/getting-started
    - theme: alt
      text: API Documentation
      link: /api/index
    - theme: alt
      text: Architecture
      link: /architecture

features:
  - title: Provider Abstraction
    details: Integrate new speech providers without changing API contracts or orchestration clients.
  - title: Production-Ready API
    details: Stable REST endpoints for transcription and synthesis with deterministic response behavior.
  - title: Library + Service Model
    details: Use lavoix as an embedded Python client dependency or as a networked FastAPI service.
  - title: Operational Fallbacks
    details: Combine cloud-first quality with local/offline fallback strategies.
  - title: Typed Configuration
    details: Explicit environment and schema contracts reduce deployment ambiguity.
  - title: Stack Integration
    details: Native fit for seal + otter voice pipelines while remaining standalone.
---

## Product Context

lavoix is the speech transformation layer in the stack:

- `seal` captures user voice intent.
- `otter` orchestrates queueing and execution.
- `lavoix` transforms voice/audio with consistent output semantics.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,tts-oss]"
lavoix-server
```

Continue with [Getting Started](/tutorials/getting-started), then [Architecture](/architecture), then [REST API](/api/rest-api).
