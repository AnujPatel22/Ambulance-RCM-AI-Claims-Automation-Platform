from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, init_db
from app.models import Claim, Denial, PCRDocument, PayerRule


def find_data_dir() -> Path:
    settings = get_settings()
    candidates: list[Path] = []
    if settings.synthetic_data_dir:
        candidates.append(Path(settings.synthetic_data_dir))

    here = Path(__file__).resolve()
    candidates.append(Path.cwd() / "data" / "synthetic")
    candidates.extend(parent / "data" / "synthetic" for parent in here.parents)
    candidates.append(Path("/app/data/synthetic"))
    for candidate in candidates:
        if (candidate / "claims.json").exists():
            return candidate
    raise FileNotFoundError("Could not locate data/synthetic seed files")


def load_json(name: str) -> list[dict[str, Any]]:
    path = find_data_dir() / name
    return json.loads(path.read_text(encoding="utf-8"))


def upsert(db: Session, model: type, item_id: str, values: dict[str, Any]) -> None:
    existing = db.get(model, item_id)
    if existing:
        for key, value in values.items():
            setattr(existing, key, value)
    else:
        db.add(model(**values))


def seed_database(db: Session) -> None:
    for item in load_json("pcr_transcripts.json"):
        upsert(
            db,
            PCRDocument,
            item["id"],
            {
                "id": item["id"],
                "title": item["title"],
                "transcript": item["transcript"],
                "extracted_fields": {},
            },
        )
    db.commit()

    for item in load_json("claims.json"):
        upsert(db, Claim, item["id"], item)
    db.commit()

    for item in load_json("payer_rules.json"):
        upsert(db, PayerRule, item["id"], item)
    db.commit()

    for item in load_json("denials.json"):
        values = dict(item)
        if isinstance(values.get("denial_date"), str):
            values["denial_date"] = date.fromisoformat(values["denial_date"])
        upsert(db, Denial, item["id"], values)

    db.commit()


def main() -> None:
    init_db()
    with SessionLocal() as db:
        seed_database(db)
    print("Seed data loaded")


if __name__ == "__main__":
    main()
