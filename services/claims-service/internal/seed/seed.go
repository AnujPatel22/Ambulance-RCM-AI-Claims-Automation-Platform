package seed

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"

	"github.com/jackc/pgx/v5/pgxpool"
)

type pcrSeed struct {
	ID         string `json:"id"`
	Title      string `json:"title"`
	Transcript string `json:"transcript"`
}

type claimSeed struct {
	ID                 string   `json:"id"`
	PCRID              *string  `json:"pcr_id"`
	PatientLabel       string   `json:"patient_label"`
	Payer              string   `json:"payer"`
	PayerType          string   `json:"payer_type"`
	HCPCSCode          string   `json:"hcpcs_code"`
	IncidentType       string   `json:"incident_type"`
	PickupLocation     string   `json:"pickup_location"`
	Destination        string   `json:"destination"`
	Mileage            *float64 `json:"mileage"`
	MedicalNecessity   string   `json:"medical_necessity"`
	SignaturePresent   bool     `json:"signature_present"`
	SignatureException string   `json:"signature_exception"`
	Status             string   `json:"status"`
	BilledAmount       float64  `json:"billed_amount"`
}

type ruleSeed struct {
	ID             string   `json:"id"`
	Payer          string   `json:"payer"`
	PayerType      string   `json:"payer_type"`
	HCPCSCode      string   `json:"hcpcs_code"`
	DenialReason   string   `json:"denial_reason"`
	Title          string   `json:"title"`
	RuleText       string   `json:"rule_text"`
	RequiredFields []string `json:"required_fields"`
	Keywords       []string `json:"keywords"`
}

type denialSeed struct {
	ID              string   `json:"id"`
	ClaimID         string   `json:"claim_id"`
	Payer           string   `json:"payer"`
	Reason          string   `json:"reason"`
	Status          string   `json:"status"`
	MissingEvidence []string `json:"missing_evidence"`
	DenialDate      string   `json:"denial_date"`
}

func Seed(ctx context.Context, pool *pgxpool.Pool) error {
	dir, err := findDataDir()
	if err != nil {
		return err
	}

	var pcrs []pcrSeed
	if err := readJSON(filepath.Join(dir, "pcr_transcripts.json"), &pcrs); err != nil {
		return err
	}
	for _, item := range pcrs {
		if _, err := pool.Exec(ctx, `
INSERT INTO pcr_documents (id, title, transcript, extracted_fields)
VALUES ($1, $2, $3, '{}'::jsonb)
ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, transcript = EXCLUDED.transcript
`, item.ID, item.Title, item.Transcript); err != nil {
			return err
		}
	}

	var claims []claimSeed
	if err := readJSON(filepath.Join(dir, "claims.json"), &claims); err != nil {
		return err
	}
	for _, item := range claims {
		if _, err := pool.Exec(ctx, `
INSERT INTO claims (
    id, pcr_id, patient_label, payer, payer_type, hcpcs_code, incident_type, pickup_location,
    destination, mileage, medical_necessity, signature_present, signature_exception, status, billed_amount
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
ON CONFLICT (id) DO UPDATE SET
    pcr_id = EXCLUDED.pcr_id,
    patient_label = EXCLUDED.patient_label,
    payer = EXCLUDED.payer,
    payer_type = EXCLUDED.payer_type,
    hcpcs_code = EXCLUDED.hcpcs_code,
    incident_type = EXCLUDED.incident_type,
    pickup_location = EXCLUDED.pickup_location,
    destination = EXCLUDED.destination,
    mileage = EXCLUDED.mileage,
    medical_necessity = EXCLUDED.medical_necessity,
    signature_present = EXCLUDED.signature_present,
    signature_exception = EXCLUDED.signature_exception,
    status = EXCLUDED.status,
    billed_amount = EXCLUDED.billed_amount
`, item.ID, item.PCRID, item.PatientLabel, item.Payer, item.PayerType, item.HCPCSCode, item.IncidentType,
			item.PickupLocation, item.Destination, item.Mileage, item.MedicalNecessity, item.SignaturePresent,
			item.SignatureException, item.Status, item.BilledAmount); err != nil {
			return err
		}
	}

	var rules []ruleSeed
	if err := readJSON(filepath.Join(dir, "payer_rules.json"), &rules); err != nil {
		return err
	}
	for _, item := range rules {
		requiredFields, _ := json.Marshal(item.RequiredFields)
		keywords, _ := json.Marshal(item.Keywords)
		if _, err := pool.Exec(ctx, `
INSERT INTO payer_rules (
    id, payer, payer_type, hcpcs_code, denial_reason, title, rule_text, required_fields, keywords
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9::jsonb)
ON CONFLICT (id) DO UPDATE SET
    payer = EXCLUDED.payer,
    payer_type = EXCLUDED.payer_type,
    hcpcs_code = EXCLUDED.hcpcs_code,
    denial_reason = EXCLUDED.denial_reason,
    title = EXCLUDED.title,
    rule_text = EXCLUDED.rule_text,
    required_fields = EXCLUDED.required_fields,
    keywords = EXCLUDED.keywords
`, item.ID, item.Payer, item.PayerType, item.HCPCSCode, item.DenialReason, item.Title, item.RuleText,
			string(requiredFields), string(keywords)); err != nil {
			return err
		}
	}

	var denials []denialSeed
	if err := readJSON(filepath.Join(dir, "denials.json"), &denials); err != nil {
		return err
	}
	for _, item := range denials {
		missingEvidence, _ := json.Marshal(item.MissingEvidence)
		if _, err := pool.Exec(ctx, `
INSERT INTO denials (id, claim_id, payer, reason, status, missing_evidence, denial_date)
VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7::date)
ON CONFLICT (id) DO UPDATE SET
    claim_id = EXCLUDED.claim_id,
    payer = EXCLUDED.payer,
    reason = EXCLUDED.reason,
    status = EXCLUDED.status,
    missing_evidence = EXCLUDED.missing_evidence,
    denial_date = EXCLUDED.denial_date
`, item.ID, item.ClaimID, item.Payer, item.Reason, item.Status, string(missingEvidence), item.DenialDate); err != nil {
			return err
		}
	}

	return nil
}

func readJSON(path string, out any) error {
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, out)
}

func findDataDir() (string, error) {
	candidates := []string{
		filepath.Join(".", "data", "synthetic"),
		filepath.Join("..", "..", "data", "synthetic"),
		filepath.Join("..", "..", "..", "data", "synthetic"),
		filepath.Join("/app", "data", "synthetic"),
	}
	for _, candidate := range candidates {
		if _, err := os.Stat(filepath.Join(candidate, "claims.json")); err == nil {
			return candidate, nil
		}
	}
	return "", os.ErrNotExist
}
