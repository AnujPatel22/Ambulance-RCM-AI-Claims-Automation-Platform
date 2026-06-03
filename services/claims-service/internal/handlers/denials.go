package handlers

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"time"

	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/models"
)

func (h *Handler) ListDenials(w http.ResponseWriter, r *http.Request) {
	rows, err := h.pool.Query(r.Context(), `
SELECT id, claim_id, payer, reason, status, missing_evidence, denial_date
FROM denials
ORDER BY denial_date DESC, id
`)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	defer rows.Close()

	denials := make([]models.Denial, 0)
	for rows.Next() {
		denial, err := scanDenial(rows.Scan)
		if err != nil {
			writeError(w, http.StatusInternalServerError, err.Error())
			return
		}
		denials = append(denials, denial)
	}
	writeJSON(w, http.StatusOK, denials)
}

func (h *Handler) GetDenial(w http.ResponseWriter, r *http.Request) {
	row := h.pool.QueryRow(r.Context(), `
SELECT id, claim_id, payer, reason, status, missing_evidence, denial_date
FROM denials
WHERE id = $1
`, r.PathValue("id"))
	denial, err := scanDenial(row.Scan)
	if err != nil {
		writeError(w, http.StatusNotFound, "denial not found")
		return
	}
	claim, err := h.fetchClaim(r.Context(), denial.ClaimID)
	if err == nil {
		denial.Claim = &claim
	}
	writeJSON(w, http.StatusOK, denial)
}

type denialScanner func(dest ...any) error

func scanDenial(scan denialScanner) (models.Denial, error) {
	var denial models.Denial
	var evidenceJSON []byte
	var denialDate sql.NullTime
	if err := scan(
		&denial.ID,
		&denial.ClaimID,
		&denial.Payer,
		&denial.Reason,
		&denial.Status,
		&evidenceJSON,
		&denialDate,
	); err != nil {
		return denial, err
	}
	_ = json.Unmarshal(evidenceJSON, &denial.MissingEvidence)
	if denialDate.Valid {
		dateOnly := time.Date(
			denialDate.Time.Year(),
			denialDate.Time.Month(),
			denialDate.Time.Day(),
			0,
			0,
			0,
			0,
			time.UTC,
		)
		denial.DenialDate = &dateOnly
	}
	return denial, nil
}
