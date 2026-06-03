from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class PCRFields(BaseModel):
    chief_complaint: str = ""
    incident_type: str = ""
    pickup_location: str = ""
    destination: str = ""
    vitals: list[str] = Field(default_factory=list)
    interventions: list[str] = Field(default_factory=list)
    mileage: float | None = None
    medical_necessity: str = ""
    signature_present: bool = False
    signature_exception: str = ""
    payer_type: str = ""
    crew_notes: str = ""


class PCRExtractionRequest(BaseModel):
    transcript: str
    persist: bool = False
    pcr_id: str | None = None
    title: str | None = None


class PCRExtractionResponse(BaseModel):
    pcr_id: str | None = None
    fields: PCRFields
    warnings: list[str] = Field(default_factory=list)


class PCRSample(BaseModel):
    id: str
    title: str
    transcript: str


class PayerRuleOut(BaseModel):
    id: str
    payer: str
    payer_type: str
    hcpcs_code: str
    denial_reason: str
    title: str
    rule_text: str
    required_fields: list[str]
    keywords: list[str]
    score: int | None = None


class RAGSearchRequest(BaseModel):
    query: str | None = None
    payer: str | None = None
    hcpcs_code: str | None = None
    denial_reason: str | None = None
    keywords: list[str] = Field(default_factory=list)
    limit: int = 5


class RAGSearchResponse(BaseModel):
    rules: list[PayerRuleOut]
    query_summary: str


class AppealGenerateRequest(BaseModel):
    denial_id: str | None = None
    claim_id: str | None = None
    denial_reason: str | None = None
    missing_evidence: list[str] = Field(default_factory=list)
    extra_context: str = ""


class AppealGenerateResponse(BaseModel):
    appeal_id: str
    denial_id: str | None = None
    claim_id: str | None = None
    letter_text: str
    cited_rules: list[PayerRuleOut]
    llm_provider: str


class AnalyticsSummary(BaseModel):
    total_claims: int
    total_denials: int
    high_denial_risk_claims: int
    missing_documentation_count: int
    denial_rate_reduction_percent: int = 67
    risk_before_validation: float = 0.42
    risk_after_validation: float = 0.14
    manual_resolution_days: int = 14
    automated_resolution_days: int = 2
    appeals_generated: int


class ClaimCreateRequest(BaseModel):
    pcr_id: str | None = None
    patient_label: str = "Synthetic Patient"
    payer: str = "Metro Medicare Advantage"
    payer_type: str = "Medicare Advantage"
    hcpcs_code: str = "A0427"
    incident_type: str = ""
    pickup_location: str = ""
    destination: str = ""
    mileage: float | None = None
    medical_necessity: str = ""
    signature_present: bool = False
    signature_exception: str = ""
    status: str = "prebill"
    billed_amount: float = 0


class ClaimOut(ClaimCreateRequest):
    id: str
    created_at: datetime | None = None


class DenialOut(BaseModel):
    id: str
    claim_id: str
    payer: str
    reason: str
    status: str
    missing_evidence: list[str]
    denial_date: date | None = None


class ValidationResultOut(BaseModel):
    claim_id: str
    denial_risk_score: float
    denial_risk_level: str
    missing_requirements: list[str]
    recommended_fixes: list[str]
    cited_rule_ids: list[str]


JsonDict = dict[str, Any]
