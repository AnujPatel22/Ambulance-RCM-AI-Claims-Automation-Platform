package rules

import (
	"math"
	"strings"

	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/models"
)

var fieldLabels = map[string]string{
	"incident_type":          "Incident type",
	"destination":            "Destination",
	"medical_necessity":      "Detailed medical necessity statement",
	"interventions":          "Documented intervention or monitoring",
	"vitals":                 "Assessment findings or vitals",
	"pickup_location":        "Pickup location",
	"mileage":                "Loaded mileage confirmation",
	"signature_or_exception": "Patient signature or valid signature exception",
}

var fixes = map[string]string{
	"incident_type":          "Document whether the transport was emergency or non-emergency.",
	"destination":            "Add the receiving facility or covered destination.",
	"medical_necessity":      "Document why ambulance transport was medically necessary.",
	"interventions":          "Add crew interventions or monitoring performed during transport.",
	"vitals":                 "Add assessment findings or vitals supporting the transport level.",
	"pickup_location":        "Add the pickup location or origin.",
	"mileage":                "Confirm loaded mileage in PCR and billing record.",
	"signature_or_exception": "Add patient signature, representative signature, or exception reason.",
}

func ValidateClaim(claim models.Claim, payerRules []models.PayerRule) models.ValidationResult {
	missingKeys := make([]string, 0)
	citedRuleIDs := make([]string, 0)

	for _, field := range []string{"pickup_location", "destination", "mileage", "medical_necessity", "signature_or_exception"} {
		if fieldMissing(claim, field) {
			missingKeys = append(missingKeys, field)
		}
	}

	for _, rule := range payerRules {
		citedRuleIDs = append(citedRuleIDs, rule.ID)
		for _, field := range rule.RequiredFields {
			if fieldMissing(claim, field) {
				missingKeys = append(missingKeys, field)
			}
		}
	}

	uniqueKeys := unique(missingKeys)
	score := math.Min(0.98, 0.15+(float64(len(uniqueKeys))*0.16))
	level := "Low"
	if score >= 0.45 {
		level = "High"
	} else if score >= 0.30 {
		level = "Medium"
	}

	missingRequirements := make([]string, 0, len(uniqueKeys))
	recommendedFixes := make([]string, 0, len(uniqueKeys))
	for _, key := range uniqueKeys {
		missingRequirements = append(missingRequirements, labelFor(key))
		recommendedFixes = append(recommendedFixes, fixFor(key))
	}

	return models.ValidationResult{
		ClaimID:             claim.ID,
		DenialRiskScore:     math.Round(score*100) / 100,
		DenialRiskLevel:     level,
		MissingRequirements: missingRequirements,
		RecommendedFixes:    recommendedFixes,
		CitedRuleIDs:         citedRuleIDs,
	}
}

func fieldMissing(claim models.Claim, field string) bool {
	switch field {
	case "pickup_location":
		return strings.TrimSpace(claim.PickupLocation) == ""
	case "destination":
		return strings.TrimSpace(claim.Destination) == ""
	case "incident_type":
		return strings.TrimSpace(claim.IncidentType) == ""
	case "mileage":
		return claim.Mileage == nil || *claim.Mileage <= 0
	case "medical_necessity":
		return strings.TrimSpace(claim.MedicalNecessity) == ""
	case "signature_or_exception":
		return !claim.SignaturePresent && strings.TrimSpace(claim.SignatureException) == ""
	case "vitals":
		return !containsAny(claim.MedicalNecessity, []string{"vital", "oxygen", "pulse", "blood pressure", "tachycardia"})
	case "interventions":
		return !containsAny(claim.MedicalNecessity, []string{"oxygen", "monitoring", "aspirin", "stretcher", "intervention"})
	default:
		return false
	}
}

func containsAny(value string, needles []string) bool {
	lower := strings.ToLower(value)
	for _, needle := range needles {
		if strings.Contains(lower, needle) {
			return true
		}
	}
	return false
}

func unique(values []string) []string {
	seen := map[string]bool{}
	result := make([]string, 0, len(values))
	for _, value := range values {
		if value == "" || seen[value] {
			continue
		}
		seen[value] = true
		result = append(result, value)
	}
	return result
}

func labelFor(key string) string {
	if label, ok := fieldLabels[key]; ok {
		return label
	}
	return strings.ReplaceAll(key, "_", " ")
}

func fixFor(key string) string {
	if fix, ok := fixes[key]; ok {
		return fix
	}
	return "Review " + strings.ReplaceAll(key, "_", " ") + "."
}
