from __future__ import annotations

import re
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PayerRule


class RAGEngine:
    def search(
        self,
        db: Session,
        query: str | None = None,
        payer: str | None = None,
        hcpcs_code: str | None = None,
        denial_reason: str | None = None,
        keywords: list[str] | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        rules = list(db.execute(select(PayerRule)).scalars())
        scored: list[tuple[int, PayerRule]] = []
        keyword_terms = [term.lower() for term in (keywords or []) if term.strip()]
        query_terms = self._terms(query or "")

        for rule in rules:
            score = 0
            haystack = " ".join(
                [
                    rule.payer,
                    rule.payer_type,
                    rule.hcpcs_code,
                    rule.denial_reason,
                    rule.title,
                    rule.rule_text,
                    " ".join(rule.keywords or []),
                ]
            ).lower()

            if payer and payer.lower() == rule.payer.lower():
                score += 8
            elif payer and payer.lower() in haystack:
                score += 3

            if hcpcs_code and (rule.hcpcs_code == hcpcs_code or rule.hcpcs_code == "ALL"):
                score += 5

            if denial_reason and denial_reason.lower() in rule.denial_reason.lower():
                score += 6
            elif denial_reason and any(term in haystack for term in self._terms(denial_reason)):
                score += 3

            score += sum(2 for term in keyword_terms if term in haystack)
            score += sum(1 for term in query_terms if term in haystack)

            if score > 0 or not any([query, payer, hcpcs_code, denial_reason, keyword_terms]):
                scored.append((score, rule))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [self._to_dict(rule, score) for score, rule in scored[: max(1, min(limit, 10))]]

    def _terms(self, text: str) -> list[str]:
        return [term for term in re.findall(r"[a-z0-9]+", text.lower()) if len(term) > 2]

    def _to_dict(self, rule: PayerRule, score: int) -> dict[str, Any]:
        return {
            "id": rule.id,
            "payer": rule.payer,
            "payer_type": rule.payer_type,
            "hcpcs_code": rule.hcpcs_code,
            "denial_reason": rule.denial_reason,
            "title": rule.title,
            "rule_text": rule.rule_text,
            "required_fields": rule.required_fields or [],
            "keywords": rule.keywords or [],
            "score": score,
        }
