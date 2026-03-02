# Concepts

## Provider-Driven Speech Infrastructure

Speech systems evolve quickly: model quality, pricing, latency, and availability all shift over time. lavoix treats providers as pluggable modules so product contracts remain stable while engines evolve.

## Deterministic Service Contract

The service exposes a compact, stable interface:

- `GET /healthz`
- `POST /v1/stt/transcribe`
- `POST /v1/tts/synthesize`

Keeping the interface small improves operability, testing depth, and downstream integration reliability.

## Fallback Strategy as Product Behavior

Fallback is not just an implementation detail; it is part of product behavior:

- Primary provider delivers best quality.
- Secondary provider preserves continuity when the primary path degrades.
- Explicit provider selection allows controlled experimentation and canary rollout.

## Typed Configuration

`Settings` in `src/lavoix/config.py` defines the deploy-time contract:

- host/port
- API keys and model names
- default STT/TTS providers

This lowers configuration ambiguity and helps detect drift across environments.

## Operational Concepts

### Service-level health

Health checks should include:

- process liveliness
- provider credential validity
- external API reachability (if cloud provider is required)

### Failure classes

- authentication/configuration failures
- provider capability mismatch
- dependency/runtime-level failures

Each class should be visible in logs and mapped to actionable runbook steps.
