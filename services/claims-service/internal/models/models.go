package models

import "time"

type Claim struct {
	ID                 string     `json:"id"`
	PCRID              *string    `json:"pcr_id,omitempty"`
	PatientLabel       string     `json:"patient_label"`
	Payer              string     `json:"payer"`
	PayerType          string     `json:"payer_type"`
	HCPCSCode          string     `json:"hcpcs_code"`
	IncidentType       string     `json:"incident_type"`
	PickupLocation     string     `json:"pickup_location"`
	Destination        string     `json:"destination"`
	Mileage            *float64   `json:"mileage"`
	MedicalNecessity   string     `json:"medical_necessity"`
	SignaturePresent   bool       `json:"signature_present"`
	SignatureException string     `json:"signature_exception"`
	Status             string     `json:"status"`
	BilledAmount       float64    `json:"billed_amount"`
	CreatedAt          *time.Time `json:"created_at,omitempty"`
}

type ClaimCreateRequest struct {
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

type PayerRule struct {
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

type Denial struct {
	ID              string     `json:"id"`
	ClaimID         string     `json:"claim_id"`
	Payer           string     `json:"payer"`
	Reason          string     `json:"reason"`
	Status          string     `json:"status"`
	MissingEvidence []string   `json:"missing_evidence"`
	DenialDate      *time.Time `json:"denial_date,omitempty"`
	Claim           *Claim     `json:"claim,omitempty"`
}

type ValidationResult struct {
	ClaimID             string   `json:"claim_id"`
	DenialRiskScore     float64  `json:"denial_risk_score"`
	DenialRiskLevel     string   `json:"denial_risk_level"`
	MissingRequirements []string `json:"missing_requirements"`
	RecommendedFixes    []string `json:"recommended_fixes"`
	CitedRuleIDs         []string `json:"cited_rule_ids"`
}
