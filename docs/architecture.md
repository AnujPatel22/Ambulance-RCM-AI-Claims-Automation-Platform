# Architecture

The platform is a three-service monorepo backed by PostgreSQL.

```text
Browser
  |
  | Vite React app
  v
Claims Service (Go) ---- PostgreSQL
  |                         ^
  | appeal / RAG requests   |
  v                         |
AI Service (FastAPI) --------
```

## Services

- Frontend: React, TypeScript, Vite, plain CSS.
- AI service: FastAPI for PCR extraction, payer-rule retrieval, appeal generation, and analytics.
- Claims service: Go HTTP API for claims, denials, and validation.
- Database: PostgreSQL tables for synthetic claims, rules, denials, PCR documents, appeals, and validation results.

## Data Flow

1. A synthetic EMS transcript is submitted to the AI service.
2. The AI service returns structured PCR fields using deterministic extraction plus optional LLM fallback.
3. The claims service validates claims against required fields and payer rules stored in PostgreSQL.
4. Denied claims can be sent to the AI service for RAG rule retrieval and appeal generation.
5. The frontend combines all service outputs into a recruiter-friendly demo workflow.
