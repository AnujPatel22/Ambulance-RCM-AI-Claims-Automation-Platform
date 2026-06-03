# Database Schema

The database is PostgreSQL. The AI service creates tables on startup and seeds synthetic data idempotently.

## Tables

- `pcr_documents`: synthetic EMS transcripts and extracted PCR fields.
- `claims`: ambulance claim details used by the claims queue.
- `payer_rules`: synthetic payer requirements and searchable rule text.
- `denials`: synthetic denied claim records.
- `appeal_letters`: generated synthetic appeal letters.
- `validation_results`: stored outputs from pre-bill claim validation.

JSONB columns are used for extracted PCR fields, required rule fields, missing evidence lists, citations, and validation recommendations.
