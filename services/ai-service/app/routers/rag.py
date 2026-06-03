from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RAGSearchRequest, RAGSearchResponse
from app.services.rag_engine import RAGEngine

router = APIRouter(prefix="/rag", tags=["rag"])
rag_engine = RAGEngine()


@router.post("/search", response_model=RAGSearchResponse)
def search(request: RAGSearchRequest, db: Session = Depends(get_db)) -> RAGSearchResponse:
    rules = rag_engine.search(
        db,
        query=request.query,
        payer=request.payer,
        hcpcs_code=request.hcpcs_code,
        denial_reason=request.denial_reason,
        keywords=request.keywords,
        limit=request.limit,
    )
    summary_parts = [
        value
        for value in [request.payer, request.hcpcs_code, request.denial_reason, request.query]
        if value
    ]
    return RAGSearchResponse(
        rules=rules,
        query_summary=", ".join(summary_parts) if summary_parts else "all synthetic payer rules",
    )
