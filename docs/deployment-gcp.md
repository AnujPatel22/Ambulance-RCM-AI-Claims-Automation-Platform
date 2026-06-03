# GCP-Style Deployment Notes

This repo is designed for local Docker Compose first. A production-style GCP deployment could use:

- Cloud Run for the FastAPI AI service.
- Cloud Run for the Go claims service.
- Cloud Run or Firebase Hosting for the React frontend.
- Cloud SQL for PostgreSQL.
- Secret Manager for database credentials and LLM API keys.
- Cloud Build or GitHub Actions for CI/CD.

## Example High-Level Flow

1. Build each service image.
2. Push images to Artifact Registry.
3. Provision Cloud SQL PostgreSQL.
4. Store secrets in Secret Manager.
5. Deploy backend services to Cloud Run with Cloud SQL connectivity.
6. Deploy frontend with environment variables pointing to backend service URLs.

These notes are intentionally GCP-style documentation, not a production compliance checklist.
