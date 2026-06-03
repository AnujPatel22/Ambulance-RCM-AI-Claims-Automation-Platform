package tests

import (
	"testing"

	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/models"
	"ambulance-rcm-ai-claims-platform/services/claims-service/internal/rules"
)

func TestValidateClaimFlagsMissingMileageAndSignature(t *testing.T) {
	claim := models.Claim{
		ID:               "CLM-TEST",
		PickupLocation:   "Patient home",
		Destination:      "Valley Medical Center",
		MedicalNecessity: "Shortness of breath requiring oxygen.",
		SignaturePresent: false,
	}
	payerRules := []models.PayerRule{
		{
			ID:             "RULE-1",
			RequiredFields: []string{"mileage", "signature_or_exception", "medical_necessity"},
		},
	}

	result := rules.ValidateClaim(claim, payerRules)

	if result.DenialRiskLevel != "Medium" && result.DenialRiskLevel != "High" {
		t.Fatalf("expected medium or high risk, got %s", result.DenialRiskLevel)
	}
	assertContains(t, result.MissingRequirements, "Loaded mileage confirmation")
	assertContains(t, result.MissingRequirements, "Patient signature or valid signature exception")
	assertContains(t, result.CitedRuleIDs, "RULE-1")
}

func TestValidateClaimLowRiskWhenRequirementsPresent(t *testing.T) {
	mileage := 8.2
	claim := models.Claim{
		ID:                 "CLM-TEST",
		PickupLocation:     "Clinic",
		Destination:        "Hospital",
		Mileage:            &mileage,
		MedicalNecessity:   "Acute symptoms with pulse elevation and monitoring during transport.",
		SignaturePresent:   false,
		SignatureException: "Patient refused; witnessed by staff.",
	}
	result := rules.ValidateClaim(claim, []models.PayerRule{{ID: "RULE-1", RequiredFields: []string{"vitals"}}})

	if result.DenialRiskLevel != "Low" {
		t.Fatalf("expected low risk, got %s", result.DenialRiskLevel)
	}
	if len(result.MissingRequirements) != 0 {
		t.Fatalf("expected no missing requirements, got %v", result.MissingRequirements)
	}
}

func assertContains(t *testing.T, values []string, expected string) {
	t.Helper()
	for _, value := range values {
		if value == expected {
			return
		}
	}
	t.Fatalf("expected %q in %v", expected, values)
}
