# Contributing

This repository is a public portfolio project. Keep changes scoped, tested, and synthetic-data safe.

## Checks

Run relevant service tests before committing:

```bash
cd services/claims-service
go test ./...
```

```bash
cd services/ai-service
pytest
```

## Data Safety

- No PHI.
- No real EMS records.
- No real payer contracts.
- No real member IDs.
- No secrets.
