#!/usr/bin/env bash
set -euo pipefail

echo "Seeding synthetic ambulance RCM data..."
docker compose run --rm ai-service python -m app.seed
echo "Seed complete."
