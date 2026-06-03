# Security and Compliance

This project is a portfolio MVP and uses only synthetic data.

## Not Production Ready

It is not a medical device, billing system, payer decision engine, or compliance product. A production version would require HIPAA review, legal review, security controls, audit logging, access control, encryption, PHI redaction, secure key management, and human oversight.

## Data Safety

- Do not submit real patient data.
- Do not upload real medical records.
- Do not store PHI in this repository.
- Keep API keys in `.env`, not in source control.

## LLM Safety

The LLM client has a mock fallback so the app works without external AI calls. Any real LLM integration should include PHI safeguards, redaction, logging controls, and vendor compliance review.
