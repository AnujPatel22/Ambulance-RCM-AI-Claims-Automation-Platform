package config

import "os"

type Config struct {
	DatabaseURL        string
	Port               string
	CORSAllowedOrigins string
}

func Load() Config {
	return Config{
		DatabaseURL:        getenv("DATABASE_URL", "postgres://ambulance:ambulance@localhost:5432/ambulance_rcm?sslmode=disable"),
		Port:               getenv("PORT", "8080"),
		CORSAllowedOrigins: getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173"),
	}
}

func getenv(key, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	return value
}
