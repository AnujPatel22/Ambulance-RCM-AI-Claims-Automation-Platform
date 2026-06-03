# Testing and QA

## Local Test Commands

```bash
make test
```

Or run individual suites:

```bash
make test-ai
make test-go
make test-frontend
```

## Coverage Focus

- PCR extraction works for representative synthetic narratives.
- Claim validation flags missing mileage, signatures, medical necessity, and payer requirements.
- Appeal generation works without a real LLM key.
- Frontend TypeScript checks pass.

## Manual QA

Run `docker compose up --build`, open the frontend, and complete the README demo walkthrough.
