package main

import (
	"context"
	"log"
	"net/http"

	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/config"
	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/db"
	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/handlers"
	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/seed"
)

func main() {
	cfg := config.Load()
	ctx := context.Background()

	pool, err := db.Connect(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("database connection failed: %v", err)
	}
	defer pool.Close()

	if err := db.EnsureSchema(ctx, pool); err != nil {
		log.Fatalf("schema initialization failed: %v", err)
	}
	if err := seed.Seed(ctx, pool); err != nil {
		log.Fatalf("seed failed: %v", err)
	}

	handler := handlers.New(pool)
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", handler.Health)
	mux.HandleFunc("GET /claims", handler.ListClaims)
	mux.HandleFunc("POST /claims", handler.CreateClaim)
	mux.HandleFunc("GET /claims/{id}", handler.GetClaim)
	mux.HandleFunc("POST /claims/{id}/validate", handler.ValidateClaim)
	mux.HandleFunc("GET /denials", handler.ListDenials)
	mux.HandleFunc("GET /denials/{id}", handler.GetDenial)

	addr := ":" + cfg.Port
	log.Printf("claims-service listening on %s", addr)
	if err := http.ListenAndServe(addr, cors(cfg.CORSAllowedOrigins, mux)); err != nil {
		log.Fatal(err)
	}
}

func cors(allowedOrigin string, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		origin := allowedOrigin
		if origin == "" {
			origin = "*"
		}
		w.Header().Set("Access-Control-Allow-Origin", origin)
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}
