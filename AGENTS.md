# AGENTS.md

## Project Identity

This repository is an Ambulance RCM & AI Claims Automation Platform. It simulates how EMS agencies can use AI to improve revenue-cycle workflows, reduce claim denials, extract structured PCR information, validate claims before submission, and automate denial appeals.

The platform must be GitHub-ready, demo-ready, and resume-ready.

## Core Stack

Use this stack unless a change is absolutely necessary:

- Frontend: React.js, TypeScript, Vite
- AI service: Python, FastAPI
- Claims service: Go
- Database: PostgreSQL
- RAG storage: PostgreSQL tables with simple text search first; optional pgvector if easy
- Deployment style: Docker Compose locally, GCP Cloud Run documentation
- LLM integration: provider-agnostic client with mock fallback

## Non-Negotiable Rules

1. Never use real patient data.
2. Never include real PHI.
3. All EMS, patient, claim, payer, and denial data must be synthetic.
4. The app must run locally with Docker Compose.
5. The app must work even when no LLM API key is provided.
6. Add practical tests.
7. Keep the code readable and easy to demo.
8. Prefer a working MVP over complex unfinished architecture.
9. Do not add huge dependencies unless needed.
10. Do not create dead links, broken commands, or fake features in the README.

## User Experience Goal

A recruiter or engineering manager should be able to clone the repo, run one command, open the UI, and understand:

- How an EMS transcript becomes structured PCR fields
- How a claim is validated before submission
- How missing payer requirements are flagged
- How denial risk is scored
- How a denial appeal is generated
- How operational metrics show denial reduction and time saved

## Main Features

Implement these features:

1. Ambient EMS documentation
   - Input: synthetic EMS narrative or transcript
   - Output: structured PCR fields
   - Fields: chief complaint, incident type, pickup location, destination, vitals, interventions, mileage, medical necessity, signatures, payer type

2. Pre-bill claim validation
   - Validate required fields
   - Compare claim data against payer rules
   - Flag missing documentation
   - Generate denial-risk score
   - Generate recommended fixes

3. Payer rule RAG
   - Store synthetic payer rules
   - Search relevant payer rules by payer, CPT/HCPCS code, denial reason, and keywords
   - Return cited rule snippets
   - Use retrieved rules in validation and appeals

4. Denial management
   - Display denied claims
   - Show denial reason, missing evidence, appeal status
   - Allow appeal generation

5. AI appeal letter generation
   - Generate appeal letters using:
     - claim details
     - denial reason
     - retrieved payer rules
     - missing evidence checklist
   - Must work with mock LLM fallback

6. Dashboard metrics
   - Total claims
   - Denial risk before validation
   - Denial risk after validation
   - Simulated denial rate reduction: 67%
   - Manual denial resolution baseline: 14 days
   - Automated appeal resolution simulation: 2 days

## Coding Standards

### Python

- Use FastAPI.
- Use Pydantic schemas.
- Keep services modular.
- Include tests with pytest.
- Keep LLM logic isolated in `llm_client.py`.
- Mock LLM output when no API key exists.

### Go

- Use net/http or chi router.
- Keep handlers simple.
- Use database/sql or pgx.
- Include validation logic in internal rules package.
- Include tests for rule validation.

### React

- Use TypeScript.
- Use clean components.
- Use a simple professional dashboard.
- Avoid over-designed UI libraries unless necessary.
- Use CSS modules or plain CSS.
- Handle loading and error states.

### Database

Use PostgreSQL with tables for:

- pcr_documents
- claims
- payer_rules
- denials
- appeal_letters
- validation_results

Seed data must make the UI immediately useful.

## Demo Flow

The finished app must support this demo flow:

1. User opens dashboard.
2. User goes to Ambient Documentation.
3. User selects or pastes an EMS transcript.
4. App extracts structured PCR fields.
5. User creates or updates a claim.
6. App validates the claim against payer rules.
7. App flags missing requirements.
8. User opens Denial Management.
9. User selects a denied claim.
10. App retrieves relevant payer rules.
11. User generates an appeal letter.
12. Dashboard shows simulated improvements.

## README Requirements

README must include:

- Project title
- Demo summary
- Architecture diagram in text
- Features
- Tech stack
- Local setup
- Docker setup
- API endpoints
- Demo walkthrough
- Synthetic data disclaimer
- Security and compliance note
- Resume bullet section
- Future improvements

## Final Completion Criteria

Before finishing, verify:

- `docker compose up --build` runs
- Frontend loads
- FastAPI docs load
- Go claims service health endpoint works
- PostgreSQL starts
- Seed data loads
- At least one PCR extraction works
- At least one claim validation works
- At least one appeal letter generates
- README is accurate
- Tests pass or failures are clearly explained
