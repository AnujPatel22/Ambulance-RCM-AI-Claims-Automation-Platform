#!/usr/bin/env bash
set -euo pipefail

AI_URL="${AI_URL:-http://localhost:8000}"
CLAIMS_URL="${CLAIMS_URL:-http://localhost:8080}"

echo "Health checks"
curl -fsS "$AI_URL/health"
echo
curl -fsS "$CLAIMS_URL/health"
echo

echo "PCR extraction"
curl -fsS "$AI_URL/documentation/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Unit Medic 12 responded to a 74-year-old female with shortness of breath and chest discomfort at home. Patient had oxygen saturation of 88 percent. Crew administered oxygen and transported patient to Valley Medical Center. Mileage was 12.4 miles. No patient signature was documented.",
    "persist": false
  }'
echo

echo "Claim validation"
curl -fsS -X POST "$CLAIMS_URL/claims/CLM-1001/validate"
echo

echo "Appeal generation"
curl -fsS "$AI_URL/appeals/generate" \
  -H "Content-Type: application/json" \
  -d '{"denial_id": "DEN-2001"}'
echo
