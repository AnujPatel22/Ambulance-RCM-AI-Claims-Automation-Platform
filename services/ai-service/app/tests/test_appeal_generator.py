from app.services.appeal_generator import AppealGenerator
from app.services.llm_client import LLMClient


class MockClient(LLMClient):
    @property
    def provider_name(self) -> str:
        return "mock"

    def generate(self, prompt: str, fallback: str) -> str:
        return fallback


def test_appeal_generator_uses_claim_denial_and_rule_context() -> None:
    claim = {
        "id": "CLM-1001",
        "payer": "Metro Medicare Advantage",
        "destination": "Valley Medical Center",
        "mileage": 12.4,
        "medical_necessity": "Abnormal oxygen saturation and oxygen administration.",
    }
    denial = {
        "reason": "Missing signature",
        "missing_evidence": ["Signature exception"],
    }
    rules = [
        {
            "id": "RULE-003",
            "rule_text": "Claims must include a signature or documented exception.",
        }
    ]

    letter = AppealGenerator(MockClient()).generate(claim, denial, rules)

    assert "CLM-1001" in letter
    assert "Missing signature" in letter
    assert "RULE-003" in letter
    assert "no real PHI" in letter
