# Backend Spec

## FastAPI AI Service

Responsibilities:

- Extract structured PCR-style fields from synthetic EMS narratives.
- Search synthetic payer rules.
- Generate appeal letters using claim, denial, and payer-rule context.
- Return dashboard analytics.
- Seed database tables at startup.

## Go Claims Service

Responsibilities:

- Serve synthetic claims and denials.
- Validate claims against common ambulance billing requirements.
- Store validation results.
- Provide a simple HTTP API for the React frontend.

Both services include CORS support for local Vite development.
