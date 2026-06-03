package handlers

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/models"
	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/rules"
)

func (h *Handler) ListClaims(w http.ResponseWriter, r *http.Request) {
	rows, err := h.pool.Query(r.Context(), `
SELECT id, pcr_id, patient_label, payer, payer_type, hcpcs_code, incident_type, pickup_location,
       destination, mileage, medical_necessity, signature_present, signature_exception, status,
       billed_amount, created_at
FROM claims
ORDER BY id
`)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	defer rows.Close()

	claims := make([]models.Claim, 0)
	for rows.Next() {
		claim, err := scanClaim(rows.Scan)
		if err != nil {
			writeError(w, http.StatusInternalServerError, err.Error())
			return
		}
		claims = append(claims, claim)
	}
	writeJSON(w, http.StatusOK, claims)
}

func (h *Handler) GetClaim(w http.ResponseWriter, r *http.Request) {
	claim, err := h.fetchClaim(r.Context(), r.PathValue("id"))
	if err != nil {
		writeError(w, http.StatusNotFound, "claim not found")
		return
	}
	writeJSON(w, http.StatusOK, claim)
}

func (h *Handler) CreateClaim(w http.ResponseWriter, r *http.Request) {
	var req models.ClaimCreateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid JSON body")
		return
	}
	applyClaimDefaults(&req)
	id := "CLM-DEMO-" + time.Now().Format("150405")

	_, err := h.pool.Exec(r.Context(), `
INSERT INTO claims (
    id, pcr_id, patient_label, payer, payer_type, hcpcs_code, incident_type, pickup_location,
    destination, mileage, medical_necessity, signature_present, signature_exception, status, billed_amount
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
`, id, req.PCRID, req.PatientLabel, req.Payer, req.PayerType, req.HCPCSCode, req.IncidentType,
		req.PickupLocation, req.Destination, req.Mileage, req.MedicalNecessity, req.SignaturePresent,
		req.SignatureException, req.Status, req.BilledAmount)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	claim, err := h.fetchClaim(r.Context(), id)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	writeJSON(w, http.StatusCreated, claim)
}

func (h *Handler) ValidateClaim(w http.ResponseWriter, r *http.Request) {
	claimID := r.PathValue("id")
	claim, err := h.fetchClaim(r.Context(), claimID)
	if err != nil {
		writeError(w, http.StatusNotFound, "claim not found")
		return
	}
	payerRules, err := h.fetchPayerRules(r.Context(), claim)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	result := rules.ValidateClaim(claim, payerRules)
	if err := h.storeValidationResult(r.Context(), result); err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	writeJSON(w, http.StatusOK, result)
}

func (h *Handler) fetchClaim(ctx context.Context, id string) (models.Claim, error) {
	row := h.pool.QueryRow(ctx, `
SELECT id, pcr_id, patient_label, payer, payer_type, hcpcs_code, incident_type, pickup_location,
       destination, mileage, medical_necessity, signature_present, signature_exception, status,
       billed_amount, created_at
FROM claims
WHERE id = $1
`, id)
	return scanClaim(row.Scan)
}

func (h *Handler) fetchPayerRules(ctx context.Context, claim models.Claim) ([]models.PayerRule, error) {
	rows, err := h.pool.Query(ctx, `
SELECT id, payer, payer_type, hcpcs_code, denial_reason, title, rule_text, required_fields, keywords
FROM payer_rules
WHERE payer = $1 AND (hcpcs_code = $2 OR hcpcs_code = 'ALL')
ORDER BY hcpcs_code DESC, id
`, claim.Payer, claim.HCPCSCode)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	items := make([]models.PayerRule, 0)
	for rows.Next() {
		var item models.PayerRule
		var requiredFieldsJSON []byte
		var keywordsJSON []byte
		if err := rows.Scan(
			&item.ID,
			&item.Payer,
			&item.PayerType,
			&item.HCPCSCode,
			&item.DenialReason,
			&item.Title,
			&item.RuleText,
			&requiredFieldsJSON,
			&keywordsJSON,
		); err != nil {
			return nil, err
		}
		_ = json.Unmarshal(requiredFieldsJSON, &item.RequiredFields)
		_ = json.Unmarshal(keywordsJSON, &item.Keywords)
		items = append(items, item)
	}
	return items, nil
}

func (h *Handler) storeValidationResult(ctx context.Context, result models.ValidationResult) error {
	missing, _ := json.Marshal(result.MissingRequirements)
	fixes, _ := json.Marshal(result.RecommendedFixes)
	citations, _ := json.Marshal(result.CitedRuleIDs)
	_, err := h.pool.Exec(ctx, `
INSERT INTO validation_results (
    id, claim_id, denial_risk_score, denial_risk_level, missing_requirements, recommended_fixes, cited_rule_ids
) VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb, $7::jsonb)
`, "VAL-"+time.Now().Format("150405000"), result.ClaimID, result.DenialRiskScore, result.DenialRiskLevel,
		string(missing), string(fixes), string(citations))
	return err
}

type scanner func(dest ...any) error

func scanClaim(scan scanner) (models.Claim, error) {
	var claim models.Claim
	var pcrID sql.NullString
	var mileage sql.NullFloat64
	var createdAt sql.NullTime

	err := scan(
		&claim.ID,
		&pcrID,
		&claim.PatientLabel,
		&claim.Payer,
		&claim.PayerType,
		&claim.HCPCSCode,
		&claim.IncidentType,
		&claim.PickupLocation,
		&claim.Destination,
		&mileage,
		&claim.MedicalNecessity,
		&claim.SignaturePresent,
		&claim.SignatureException,
		&claim.Status,
		&claim.BilledAmount,
		&createdAt,
	)
	if err != nil {
		return claim, err
	}
	if pcrID.Valid {
		claim.PCRID = &pcrID.String
	}
	if mileage.Valid {
		claim.Mileage = &mileage.Float64
	}
	if createdAt.Valid {
		claim.CreatedAt = &createdAt.Time
	}
	return claim, nil
}

func applyClaimDefaults(req *models.ClaimCreateRequest) {
	if strings.TrimSpace(req.PatientLabel) == "" {
		req.PatientLabel = "Synthetic Patient Demo"
	}
	if strings.TrimSpace(req.Payer) == "" {
		req.Payer = "Metro Medicare Advantage"
	}
	if strings.TrimSpace(req.PayerType) == "" {
		req.PayerType = "Medicare Advantage"
	}
	if strings.TrimSpace(req.HCPCSCode) == "" {
		req.HCPCSCode = "A0427"
	}
	if strings.TrimSpace(req.Status) == "" {
		req.Status = "prebill"
	}
	if req.BilledAmount == 0 {
		req.BilledAmount = 950
	}
}

func claimNotFound(id string) error {
	return fmt.Errorf("claim %s not found", id)
}
