from __future__ import annotations

from typing import Any

from app.services.llm_client import LLMClient


class AppealGenerator:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()

    def generate(
        self,
        claim: dict[str, Any],
        denial: dict[str, Any],
        rules: list[dict[str, Any]],
        extra_context: str = "",
    ) -> str:
        fallback = self._fallback_letter(claim, denial, rules, extra_context)
        prompt = self._prompt(claim, denial, rules, extra_context)
        return self.llm_client.generate(prompt, fallback)

    def _fallback_letter(
        self,
        claim: dict[str, Any],
        denial: dict[str, Any],
        rules: list[dict[str, Any]],
        extra_context: str,
    ) -> str:
        claim_id = claim.get("id", "the synthetic claim")
        payer = claim.get("payer") or denial.get("payer") or "the payer"
        denial_reason = denial.get("reason") or "the denied ambulance claim"
        medical_necessity = claim.get("medical_necessity") or "the PCR supports ambulance transport."
        destination = claim.get("destination") or "the receiving facility"
        mileage = claim.get("mileage")
        mileage_text = f" Loaded mileage was documented as {mileage} miles." if mileage else ""

        evidence = denial.get("missing_evidence") or []
        evidence_text = ""
        if evidence:
            evidence_text = " The appeal packet should address: " + "; ".join(evidence) + "."

        citations = " ".join(
            f"{rule['id']} states that {rule['rule_text']}" for rule in rules[:3] if rule.get("rule_text")
        )
        if not citations:
            citations = "The synthetic payer rules support review of medical necessity, mileage, destination, and signature documentation."

        extra = f"\n\nAdditional reviewer context: {extra_context}" if extra_context else ""

        return (
            "To the Appeals Department,\n\n"
            f"We are appealing the denial for claim {claim_id} issued by {payer}. "
            f"The denial reason was: {denial_reason}.\n\n"
            f"The EMS record supports ambulance transport because {medical_necessity} "
            f"The patient was transported to {destination}.{mileage_text}{evidence_text}\n\n"
            f"Relevant synthetic payer guidance: {citations}\n\n"
            "Please reconsider the denial based on the enclosed synthetic PCR documentation, "
            "claim record, and payer-rule evidence. This demo letter contains no real PHI."
            f"{extra}\n"
        )

    def _prompt(
        self,
        claim: dict[str, Any],
        denial: dict[str, Any],
        rules: list[dict[str, Any]],
        extra_context: str,
    ) -> str:
        return (
            "Draft a concise synthetic ambulance claim appeal letter.\n"
            f"Claim: {claim}\n"
            f"Denial: {denial}\n"
            f"Rules: {rules}\n"
            f"Extra context: {extra_context}\n"
            "Do not include real patient data or claim that this is legal advice."
        )
