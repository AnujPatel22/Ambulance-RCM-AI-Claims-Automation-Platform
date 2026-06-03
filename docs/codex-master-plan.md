# Codex Master Plan

## Goal

Build a full-stack ambulance RCM and AI claims automation platform that runs locally with Docker Compose and demonstrates:

- EMS ambient documentation extraction
- PCR field auto-population
- Pre-bill claim validation
- RAG-based payer rule retrieval
- Denial management
- Automated appeal letter generation
- Dashboard analytics

## Build Strategy

Do not attempt everything in one uncontrolled pass. Build in phases and verify after each phase.

## Phase 1 - Repository Foundation

Create:

- Monorepo folder structure
- README
- AGENTS.md
- Docker Compose
- .env.example
- .gitignore
- Makefile
- docs folder
- synthetic data folder
- CI workflow

Acceptance criteria:

- Repository structure exists
- Docker Compose file validates
- README has accurate setup instructions
- Environment variables are documented

## Phase 2 - PostgreSQL and Seed Data

Create database schema and seed data.

Tables:

- pcr_documents
- claims
- payer_rules
- denials
- appeal_letters
- validation_results

Seed:

- 5 synthetic PCR transcripts
- 8 synthetic claims
- 10 synthetic payer rules
- 5 synthetic denials

Acceptance criteria:

- PostgreSQL starts
- Seed data loads
- Claims and payer rules can be queried

## Phase 3 - Python FastAPI AI Service

Implement:

- /documentation/extract
- /rag/search
- /appeals/generate
- /analytics/summary

Services:

- pcr_extractor.py
- rag_engine.py
- claim_validator.py
- appeal_generator.py
- llm_client.py

Acceptance criteria:

- FastAPI starts on port 8000
- API docs open
- Extract endpoint returns structured PCR fields
- RAG endpoint returns relevant payer rules
- Appeal endpoint returns an appeal letter
- Mock LLM works without API key

## Phase 4 - Go Claims Service

Implement:

- /health
- /claims
- /claims/{id}
- /claims/{id}/validate
- /denials
- /denials/{id}

Acceptance criteria:

- Go service starts on port 8080
- Health endpoint works
- Claims endpoint returns seed claims
- Validation endpoint returns risk score and missing requirements

## Phase 5 - React Frontend

Create pages:

- Dashboard
- Ambient Documentation
- Claims Queue
- Denial Management
- Rules Explorer

Acceptance criteria:

- Frontend starts on port 5173
- Dashboard shows metrics
- User can run PCR extraction
- User can validate a claim
- User can view denied claims
- User can generate appeal letter
- UI is polished and professional

## Phase 6 - End-to-End Demo Flow

Implement scripts:

- scripts/seed_all.sh
- scripts/demo_flow.sh

Acceptance criteria:

- Demo commands run
- App shows complete flow
- README demo matches actual app behavior

## Phase 7 - Testing and CI

Add tests:

- Python unit tests
- Go unit tests
- Frontend type check
- GitHub Actions workflow

Acceptance criteria:

- make test works
- CI file runs lint/test/build commands
- Failures are fixed or clearly documented

## Phase 8 - Final Polish

Polish:

- README
- API docs
- UI text
- Error states
- Empty states
- Synthetic data disclaimers
- Deployment docs

Acceptance criteria:

- Repo feels professional
- No obvious placeholder text
- No broken commands
- No real PHI
- Project supports resume bullets
