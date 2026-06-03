from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


class Base(DeclarativeBase):
    pass


class PCRDocument(Base):
    __tablename__ = "pcr_documents"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), default="")
    transcript: Mapped[str] = mapped_column(Text, nullable=False)
    extracted_fields: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    pcr_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("pcr_documents.id"), nullable=True)
    patient_label: Mapped[str] = mapped_column(String(120), nullable=False)
    payer: Mapped[str] = mapped_column(String(160), nullable=False)
    payer_type: Mapped[str] = mapped_column(String(80), nullable=False)
    hcpcs_code: Mapped[str] = mapped_column(String(20), nullable=False)
    incident_type: Mapped[str] = mapped_column(String(120), default="")
    pickup_location: Mapped[str] = mapped_column(String(180), default="")
    destination: Mapped[str] = mapped_column(String(180), default="")
    mileage: Mapped[float | None] = mapped_column(Float, nullable=True)
    medical_necessity: Mapped[str] = mapped_column(Text, default="")
    signature_present: Mapped[bool] = mapped_column(Boolean, default=False)
    signature_exception: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="prebill")
    billed_amount: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )


class PayerRule(Base):
    __tablename__ = "payer_rules"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    payer: Mapped[str] = mapped_column(String(160), nullable=False)
    payer_type: Mapped[str] = mapped_column(String(80), nullable=False)
    hcpcs_code: Mapped[str] = mapped_column(String(20), nullable=False)
    denial_reason: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    rule_text: Mapped[str] = mapped_column(Text, nullable=False)
    required_fields: Mapped[list[str]] = mapped_column(JSONB, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )


class Denial(Base):
    __tablename__ = "denials"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    claim_id: Mapped[str] = mapped_column(String(40), ForeignKey("claims.id"), nullable=False)
    payer: Mapped[str] = mapped_column(String(160), nullable=False)
    reason: Mapped[str] = mapped_column(String(220), nullable=False)
    status: Mapped[str] = mapped_column(String(60), default="open")
    missing_evidence: Mapped[list[str]] = mapped_column(JSONB, default=list)
    denial_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )


class AppealLetter(Base):
    __tablename__ = "appeal_letters"

    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=lambda: new_id("APL"))
    denial_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("denials.id"), nullable=True)
    claim_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("claims.id"), nullable=True)
    letter_text: Mapped[str] = mapped_column(Text, nullable=False)
    cited_rule_ids: Mapped[list[str]] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=lambda: new_id("VAL"))
    claim_id: Mapped[str] = mapped_column(String(40), ForeignKey("claims.id"), nullable=False)
    denial_risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    denial_risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    missing_requirements: Mapped[list[str]] = mapped_column(JSONB, default=list)
    recommended_fixes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    cited_rule_ids: Mapped[list[str]] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, server_default=func.now()
    )
