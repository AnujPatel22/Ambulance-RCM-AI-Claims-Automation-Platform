# API Spec

## AI Service

Base URL: `http://localhost:8000`

- `GET /health` returns service status.
- `GET /documentation/samples` returns seeded synthetic PCR transcripts.
- `POST /documentation/extract` extracts structured PCR fields from a synthetic EMS transcript.
- `POST /rag/search` retrieves payer rules by payer, code, denial reason, or keywords.
- `POST /appeals/generate` generates and stores a synthetic appeal letter.
- `GET /analytics/summary` returns demo metrics.

## Claims Service

Base URL: `http://localhost:8080`

- `GET /health` returns service status.
- `GET /claims` returns seeded synthetic claims.
- `GET /claims/{id}` returns a claim by ID.
- `POST /claims` creates a synthetic claim from extracted PCR fields.
- `POST /claims/{id}/validate` validates a claim against payer rules.
- `GET /denials` returns seeded synthetic denials.
- `GET /denials/{id}` returns a denial by ID.

All API payloads are synthetic and must not contain real patient information.
