from app.services.claim_validator import ClaimValidator


def test_claim_validator_flags_missing_signature_and_mileage() -> None:
    claim = {
        "id": "CLM-TEST",
        "pickup_location": "Patient home",
        "destination": "Valley Medical Center",
        "mileage": None,
        "medical_necessity": "Shortness of breath requiring oxygen.",
        "signature_present": False,
        "signature_exception": "",
    }
    rules = [
        {
            "id": "RULE-TEST",
            "required_fields": ["mileage", "signature_or_exception", "medical_necessity"],
        }
    ]

    result = ClaimValidator().validate(claim, rules)

    assert result["denial_risk_level"] in {"Medium", "High"}
    assert "Loaded mileage confirmation" in result["missing_requirements"]
    assert "Patient signature or valid signature exception" in result["missing_requirements"]
    assert result["cited_rule_ids"] == ["RULE-TEST"]


def test_claim_validator_low_risk_when_required_fields_present() -> None:
    claim = {
        "id": "CLM-TEST",
        "pickup_location": "Clinic",
        "destination": "Hospital",
        "mileage": 8.2,
        "medical_necessity": "Acute symptoms and monitoring during transport.",
        "signature_present": True,
        "signature_exception": "",
        "vitals": ["pulse 118"],
        "interventions": ["Cardiac monitoring"],
    }

    result = ClaimValidator().validate(claim, [{"id": "RULE-1", "required_fields": ["vitals"]}])

    assert result["denial_risk_level"] == "Low"
    assert result["missing_requirements"] == []
