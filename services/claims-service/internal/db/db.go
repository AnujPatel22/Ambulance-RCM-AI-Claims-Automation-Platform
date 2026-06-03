package db

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

func Connect(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	var lastErr error
	for i := 0; i < 30; i++ {
		pool, err := pgxpool.New(ctx, databaseURL)
		if err == nil {
			if pingErr := pool.Ping(ctx); pingErr == nil {
				return pool, nil
			} else {
				lastErr = pingErr
				pool.Close()
			}
		} else {
			lastErr = err
		}
		time.Sleep(time.Second)
	}
	return nil, lastErr
}

func EnsureSchema(ctx context.Context, pool *pgxpool.Pool) error {
	_, err := pool.Exec(ctx, `
CREATE TABLE IF NOT EXISTS pcr_documents (
    id VARCHAR(40) PRIMARY KEY,
    title VARCHAR(200) DEFAULT '',
    transcript TEXT NOT NULL,
    extracted_fields JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS claims (
    id VARCHAR(40) PRIMARY KEY,
    pcr_id VARCHAR(40) REFERENCES pcr_documents(id),
    patient_label VARCHAR(120) NOT NULL,
    payer VARCHAR(160) NOT NULL,
    payer_type VARCHAR(80) NOT NULL,
    hcpcs_code VARCHAR(20) NOT NULL,
    incident_type VARCHAR(120) DEFAULT '',
    pickup_location VARCHAR(180) DEFAULT '',
    destination VARCHAR(180) DEFAULT '',
    mileage DOUBLE PRECISION,
    medical_necessity TEXT DEFAULT '',
    signature_present BOOLEAN DEFAULT false,
    signature_exception TEXT DEFAULT '',
    status VARCHAR(40) DEFAULT 'prebill',
    billed_amount DOUBLE PRECISION DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payer_rules (
    id VARCHAR(40) PRIMARY KEY,
    payer VARCHAR(160) NOT NULL,
    payer_type VARCHAR(80) NOT NULL,
    hcpcs_code VARCHAR(20) NOT NULL,
    denial_reason VARCHAR(200) NOT NULL,
    title VARCHAR(220) NOT NULL,
    rule_text TEXT NOT NULL,
    required_fields JSONB DEFAULT '[]'::jsonb,
    keywords JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS denials (
    id VARCHAR(40) PRIMARY KEY,
    claim_id VARCHAR(40) NOT NULL REFERENCES claims(id),
    payer VARCHAR(160) NOT NULL,
    reason VARCHAR(220) NOT NULL,
    status VARCHAR(60) DEFAULT 'open',
    missing_evidence JSONB DEFAULT '[]'::jsonb,
    denial_date DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS appeal_letters (
    id VARCHAR(40) PRIMARY KEY,
    denial_id VARCHAR(40) REFERENCES denials(id),
    claim_id VARCHAR(40) REFERENCES claims(id),
    letter_text TEXT NOT NULL,
    cited_rule_ids JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS validation_results (
    id VARCHAR(40) PRIMARY KEY,
    claim_id VARCHAR(40) NOT NULL REFERENCES claims(id),
    denial_risk_score DOUBLE PRECISION NOT NULL,
    denial_risk_level VARCHAR(40) NOT NULL,
    missing_requirements JSONB DEFAULT '[]'::jsonb,
    recommended_fixes JSONB DEFAULT '[]'::jsonb,
    cited_rule_ids JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);
`)
	return err
}
