from __future__ import annotations

from typing import Any


FIELD_LABELS = {
    "incident_type": "Incident type",
    "destination": "Destination",
    "medical_necessity": "Detailed medical necessity statement",
    "interventions": "Documented intervention or monitoring",
    "vitals": "Assessment findings or vitals",
    "pickup_location": "Pickup location",
    "mileage": "Loaded mileage confirmation",
    "signature_or_exception": "Patient signature or valid signature exception",
}

FIXES = {
    "incident_type": "Document whether the transport was emergency or non-emergency.",
    "destination": "Add the receiving facility or covered destination.",
    "medical_necessity": "Document why ambulance transport was medically necessary.",
    "interventions": "Add crew interventions or monitoring performed during transport.",
    "vitals": "Add assessment findings or vitals supporting the transport level.",
    "pickup_location": "Add the pickup location or origin.",
    "mileage": "Confirm loaded mileage in PCR and billing record.",
    "signature_or_exception": "Add patient signature, representative signature, or exception reason.",
}


class ClaimValidator:
    def validate(self, claim: dict[str, Any], rules: list[dict[str, Any]]) -> dict[str, Any]:
        missing_keys: list[str] = []
        cited_rule_ids: list[str] = []

        baseline = ["pickup_location", "destination", "mileage", "medical_necessity", "signature_or_exception"]
        for field in baseline:
            if self._field_missing(claim, field):
                missing_keys.append(field)

        for rule in rules:
            cited_rule_ids.append(str(rule.get("id", "")))
            for field in rule.get("required_fields", []):
                if self._field_missing(claim, field):
                    missing_keys.append(field)

        unique_keys = list(dict.fromkeys(key for key in missing_keys if key))
        missing_requirements = [FIELD_LABELS.get(key, key.replace("_", " ").title()) for key in unique_keys]
        recommended_fixes = [FIXES.get(key, f"Review {key}.") for key in unique_keys]

        score = min(0.98, 0.15 + len(unique_keys) * 0.16)
        if score >= 0.45:
            level = "High"
        elif score >= 0.30:
            level = "Medium"
        else:
            level = "Low"

        return {
            "claim_id": claim.get("id", ""),
            "denial_risk_score": round(score, 2),
            "denial_risk_level": level,
            "missing_requirements": missing_requirements,
            "recommended_fixes": recommended_fixes,
            "cited_rule_ids": [rule_id for rule_id in cited_rule_ids if rule_id],
        }

    def _field_missing(self, claim: dict[str, Any], field: str) -> bool:
        if field == "signature_or_exception":
            return not bool(claim.get("signature_present")) and not bool(
                str(claim.get("signature_exception") or "").strip()
            )
        if field == "interventions":
            interventions = claim.get("interventions")
            return not bool(interventions)
        if field == "vitals":
            vitals = claim.get("vitals")
            return not bool(vitals)
        value = claim.get(field)
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (int, float)):
            return value <= 0
        if isinstance(value, list):
            return len(value) == 0
        return False
