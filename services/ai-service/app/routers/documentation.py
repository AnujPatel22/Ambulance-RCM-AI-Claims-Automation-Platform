from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PCRDocument, new_id
from app.schemas import PCRExtractionRequest, PCRExtractionResponse, PCRSample
from app.services.pcr_extractor import PCRExtractor

router = APIRouter(prefix="/documentation", tags=["documentation"])
extractor = PCRExtractor()


@router.get("/samples", response_model=list[PCRSample])
def samples(db: Session = Depends(get_db)) -> list[PCRSample]:
    docs = db.execute(select(PCRDocument).order_by(PCRDocument.id)).scalars().all()
    return [PCRSample(id=doc.id, title=doc.title, transcript=doc.transcript) for doc in docs]


@router.post("/extract", response_model=PCRExtractionResponse)
def extract(request: PCRExtractionRequest, db: Session = Depends(get_db)) -> PCRExtractionResponse:
    fields = extractor.extract(request.transcript)
    warnings = extractor.warnings(fields)
    pcr_id = request.pcr_id

    if request.persist:
        pcr_id = pcr_id or new_id("PCR")
        existing = db.get(PCRDocument, pcr_id)
        values = {
            "id": pcr_id,
            "title": request.title or "Synthetic extracted PCR",
            "transcript": request.transcript,
            "extracted_fields": fields.model_dump(),
        }
        if existing:
            for key, value in values.items():
                setattr(existing, key, value)
        else:
            db.add(PCRDocument(**values))
        db.commit()

    return PCRExtractionResponse(pcr_id=pcr_id, fields=fields, warnings=warnings)
