FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY services/claims-service/go.mod services/claims-service/go.sum ./
RUN go mod download

COPY services/claims-service ./
RUN go build -o /claims-service ./cmd/server

FROM alpine:3.20

WORKDIR /app
COPY --from=builder /claims-service /app/claims-service
COPY data ./data

EXPOSE 8080

CMD ["/app/claims-service"]
