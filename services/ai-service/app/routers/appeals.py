from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AppealLetter, Claim, Denial, new_id
from app.schemas import AppealGenerateRequest, AppealGenerateResponse
from app.services.appeal_generator import AppealGenerator
from app.services.llm_client import LLMClient
from app.services.rag_engine import RAGEngine

router = APIRouter(prefix="/appeals", tags=["appeals"])
rag_engine = RAGEngine()


def model_to_dict(obj: object) -> dict:
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.post("/generate", response_model=AppealGenerateResponse)
def generate(request: AppealGenerateRequest, db: Session = Depends(get_db)) -> AppealGenerateResponse:
    denial = db.get(Denial, request.denial_id) if request.denial_id else None
    claim_id = request.claim_id or (denial.claim_id if denial else None)
    claim = db.get(Claim, claim_id) if claim_id else None

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found for appeal generation")

    denial_dict = model_to_dict(denial) if denial else {
        "id": request.denial_id,
        "claim_id": claim.id,
        "payer": claim.payer,
        "reason": request.denial_reason or "Synthetic denial",
        "missing_evidence": request.missing_evidence,
    }
    if request.missing_evidence:
        denial_dict["missing_evidence"] = request.missing_evidence

    rules = rag_engine.search(
        db,
        payer=claim.payer,
        hcpcs_code=claim.hcpcs_code,
        denial_reason=denial_dict.get("reason"),
        keywords=denial_dict.get("missing_evidence") or [],
        limit=4,
    )

    client = LLMClient()
    letter_text = AppealGenerator(client).generate(
        model_to_dict(claim),
        denial_dict,
        rules,
        request.extra_context,
    )

    appeal = AppealLetter(
        id=new_id("APL"),
        denial_id=denial.id if denial else None,
        claim_id=claim.id,
        letter_text=letter_text,
        cited_rule_ids=[rule["id"] for rule in rules],
    )
    db.add(appeal)
    if denial:
        denial.status = "appeal_drafted"
    db.commit()

    return AppealGenerateResponse(
        appeal_id=appeal.id,
        denial_id=appeal.denial_id,
        claim_id=appeal.claim_id,
        letter_text=appeal.letter_text,
        cited_rules=rules,
        llm_provider=client.provider_name,
    )
