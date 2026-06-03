.PHONY: up down logs test test-ai test-go test-frontend build seed demo

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test: test-ai test-go test-frontend

test-ai:
	docker compose run --rm ai-service pytest -q

test-go:
	docker run --rm -v "$$(pwd)/services/claims-service:/work" -w /work golang:1.23-alpine go test ./...

test-frontend:
	docker compose run --rm frontend npm run typecheck

build:
	docker compose build

seed:
	docker compose run --rm ai-service python -m app.seed

demo:
	bash ./scripts/demo_flow.sh
