from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AppealLetter, Claim, Denial, PayerRule
from app.schemas import AnalyticsSummary
from app.services.claim_validator import ClaimValidator

router = APIRouter(prefix="/analytics", tags=["analytics"])


def claim_to_dict(claim: Claim) -> dict:
    return {column.name: getattr(claim, column.name) for column in claim.__table__.columns}


def rule_to_dict(rule: PayerRule) -> dict:
    return {column.name: getattr(rule, column.name) for column in rule.__table__.columns}


@router.get("/summary", response_model=AnalyticsSummary)
def summary(db: Session = Depends(get_db)) -> AnalyticsSummary:
    claims = db.execute(select(Claim)).scalars().all()
    rules = db.execute(select(PayerRule)).scalars().all()
    validator = ClaimValidator()
    high_risk = 0
    missing_total = 0

    for claim in claims:
        matching_rules = [
            rule
            for rule in rules
            if rule.payer == claim.payer and (rule.hcpcs_code == claim.hcpcs_code or rule.hcpcs_code == "ALL")
        ]
        result = validator.validate(claim_to_dict(claim), [rule_to_dict(rule) for rule in matching_rules])
        if result["denial_risk_level"] == "High":
            high_risk += 1
        missing_total += len(result["missing_requirements"])

    return AnalyticsSummary(
        total_claims=len(claims),
        total_denials=db.scalar(select(func.count()).select_from(Denial)) or 0,
        high_denial_risk_claims=high_risk,
        missing_documentation_count=missing_total,
        appeals_generated=db.scalar(select(func.count()).select_from(AppealLetter)) or 0,
    )
