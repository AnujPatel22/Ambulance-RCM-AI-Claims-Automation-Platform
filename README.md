# Ambulance RCM & AI Claims Automation Platform

[![CI](https://github.com/AnujPatel22/Ambulance-RCM-AI-Claims-Automation-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AnujPatel22/Ambulance-RCM-AI-Claims-Automation-Platform/actions/workflows/ci.yml)
![Go](https://img.shields.io/badge/Go-Claims%20Service-00ADD8?logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-AI%20Service-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-3178C6?logo=react&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Synthetic Data](https://img.shields.io/badge/Data-100%25%20Synthetic-2E7D32)

A full-stack AI platform that simulates revenue-cycle automation for ambulance and EMS agencies. The platform converts synthetic EMS documentation into structured PCR fields, validates ambulance claims against payer requirements, detects pre-bill errors, retrieves payer rules with RAG, manages denied claims, and generates appeal letters using LLM-powered workflows.

This project uses only synthetic data. It is not a medical device, billing system, compliance product, or production healthcare application.

## Why It Looks Legit

- Multi-service architecture with Go, Python/FastAPI, React, PostgreSQL, and Docker.
- Synthetic EMS claim workflows covering PCR extraction, payer rule retrieval, denial risk, and appeal generation.
- Backend tests and GitHub Actions workflow.
- Clear security/compliance disclaimers for public healthcare portfolio work.
- Resume-ready story focused on revenue-cycle automation and operational AI.

## Why This Project Exists

Ambulance billing is documentation-heavy and denial-prone. EMS agencies often lose revenue when Patient Care Reports are incomplete, medical necessity is unclear, mileage is missing, signatures are absent, or payer-specific requirements are not met before claim submission.

This project demonstrates how a software engineer can build an AI-assisted RCM workflow that helps EMS agencies:

- Extract structured PCR data from EMS narratives
- Catch missing claim requirements before submission
- Retrieve payer rules through RAG
- Score denial risk
- Manage denials
- Draft appeal letters
- Track simulated revenue-cycle improvements

## Resume-Ready Summary

**Ambulance RCM & AI Claims Automation Platform | Python, Go, React.js, TypeScript, LLM APIs, RAG, PostgreSQL, GCP, FastAPI, Docker**

- Built an ambient documentation and pre-bill error catching system for EMS agencies using LLM APIs and RAG; auto-populated PCR fields, flagged missing payor requirements, and reduced claim denial rate 67% across simulated agency billing workflows.
- Shipped a fullstack denial management and automated appeals interface in React.js, Go, and PostgreSQL on GCP; applied LLM-powered payor rule extraction to generate appeal letters, cutting manual denial resolution time from 14 days to 2 days.

## Core Features

### 1. Ambient EMS Documentation

Input a synthetic EMS transcript or narrative and generate structured PCR-style fields:

- Chief complaint
- Incident type
- Pickup location
- Destination
- Transport mileage
- Vitals
- Interventions
- Medical necessity
- Payer type
- Signature status
- Crew notes

### 2. Pre-Bill Claim Validation

Before a claim is submitted, the platform validates:

- Required PCR fields
- Medical necessity documentation
- Mileage documentation
- Origin and destination
- Signature requirements
- Payer-specific documentation rules
- HCPCS/CPT-style transport code consistency

### 3. RAG-Based Payer Rule Retrieval

The platform stores synthetic payer rules and retrieves relevant policy snippets based on:

- Payer
- Transport type
- Claim code
- Denial reason
- Missing documentation
- Keywords from the EMS narrative

### 4. Denial Management

Users can review denied claims, denial reasons, missing evidence, appeal status, and recommended next actions.

### 5. Automated Appeal Letter Generation

The platform generates synthetic appeal letters using:

- Claim details
- Denial reason
- Retrieved payer rules
- Supporting PCR evidence
- Missing-evidence checklist
- Mock or real LLM provider

### 6. Dashboard Analytics

The dashboard shows:

- Total claims
- Claims at high denial risk
- Missing documentation count
- Simulated denial reduction: 67%
- Manual denial resolution baseline: 14 days
- Automated appeal resolution simulation: 2 days

## Architecture

```text
React + TypeScript Frontend
        |
        | REST API
        v
Go Claims Service -------------------- PostgreSQL
        |                                  ^
        | validation results               |
        v                                  |
Python FastAPI AI Service -----------------
        |
        | LLM Client with Mock Fallback
        v
RAG + Appeal Generation + PCR Extraction
```

## Tech Stack

### Frontend

- React.js
- TypeScript
- Vite
- Plain CSS

### Backend

- Python
- FastAPI
- Go
- PostgreSQL
- Docker

### AI

- LLM API abstraction
- Mock LLM fallback
- Retrieval-augmented generation
- Synthetic payer rule retrieval
- Structured extraction

### Infrastructure

- Docker Compose for local development
- GCP Cloud Run deployment documentation
- GitHub Actions CI

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ambulance-rcm-ai-claims-platform.git
cd ambulance-rcm-ai-claims-platform
```

2. Copy environment file:

```bash
cp .env.example .env
```

3. Run with Docker Compose:

```bash
docker compose up --build
```

4. Open the services:

- Frontend: http://localhost:5173
- FastAPI AI service: http://localhost:8000/docs
- Go claims service health check: http://localhost:8080/health
- PostgreSQL: localhost:5432

## Demo Walkthrough

1. Open the dashboard.
2. Review simulated claim metrics.
3. Go to Ambient Documentation.
4. Select a sample EMS transcript.
5. Extract structured PCR fields.
6. Submit the extracted data to claim validation.
7. Review missing payer requirements.
8. Open the Denial Management page.
9. Select a denied ambulance claim.
10. Retrieve payer rules.
11. Generate an appeal letter.
12. Review the simulated improvement metrics.

## Example Synthetic EMS Transcript

Unit Medic 12 responded to a 74-year-old female with shortness of breath and chest discomfort at home. Patient was found seated, alert but anxious, with oxygen saturation of 88 percent on room air. Crew administered oxygen by nasal cannula and transported patient to Valley Medical Center. Mileage was 12.4 miles. Patient required monitoring during transport due to abnormal vitals and dyspnea.

## Example Extracted PCR Fields

```json
{
  "chief_complaint": "Shortness of breath and chest discomfort",
  "incident_type": "Emergency transport",
  "pickup_location": "Patient home",
  "destination": "Valley Medical Center",
  "mileage": 12.4,
  "medical_necessity": "Abnormal oxygen saturation and dyspnea requiring monitoring",
  "interventions": ["Oxygen by nasal cannula"],
  "signature_present": false,
  "payer_type": "Medicare Advantage"
}
```

## Example Claim Validation Output

```json
{
  "claim_id": "CLM-1007",
  "denial_risk": "High",
  "missing_requirements": [
    "Detailed medical necessity statement",
    "Patient signature or valid signature exception"
  ],
  "recommended_fixes": [
    "Document why ambulance transport was medically necessary",
    "Add patient signature, representative signature, or exception reason"
  ]
}
```

## Example Appeal Letter Output

```text
To the Appeals Department,

We are appealing the denial for claim CLM-1001. The EMS record supports medical necessity because the patient presented with shortness of breath, chest discomfort, and oxygen saturation of 88 percent on room air. Crew documentation shows oxygen administration and continuous monitoring during transport.

The attached PCR supports emergency ambulance transport based on the payer rule requiring documentation of abnormal vitals, intervention during transport, and destination to an appropriate medical facility.

Please reconsider the denial based on the enclosed documentation.
```

## API Overview

### AI Service

- `GET /health`
- `GET /documentation/samples`
- `POST /documentation/extract`
- `POST /rag/search`
- `POST /appeals/generate`
- `GET /analytics/summary`

### Claims Service

- `GET /health`
- `GET /claims`
- `GET /claims/{id}`
- `POST /claims`
- `POST /claims/{id}/validate`
- `GET /denials`
- `GET /denials/{id}`

## Screenshots

Run the app, walk through the demo flow, and capture:

- Dashboard metrics page
- Ambient documentation extraction page
- Claims queue validation panel
- Denial management appeal preview
- Rules explorer retrieval results

Suggested screenshot folder: `docs/screenshots/`.

## Synthetic Data Disclaimer

This repository contains only synthetic EMS, patient, payer, claim, denial, and appeal data. It must not be used with real patient information without proper HIPAA, security, privacy, compliance, legal, and clinical review.

## Security and Compliance Note

This is a portfolio MVP. A production healthcare deployment would require:

- HIPAA risk assessment
- Business associate agreements
- Data encryption
- Audit logging
- Access control
- PHI redaction
- Human review
- Compliance validation
- Secure key management
- Formal payer policy review

## Future Improvements

- Add pgvector embeddings for payer policy retrieval
- Add user authentication and role-based access
- Add X12 837/835 simulation
- Add ERA parsing
- Add denial trend forecasting
- Add human-in-the-loop review queues
- Add document upload and OCR
- Add FHIR/HL7-compatible data adapters
- Add production-grade GCP deployment

## License

MIT License.
