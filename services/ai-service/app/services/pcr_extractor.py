from __future__ import annotations

import re

from app.schemas import PCRFields


class PCRExtractor:
    def extract(self, transcript: str) -> PCRFields:
        text = " ".join(transcript.strip().split())
        lower = text.lower()

        mileage = self._extract_mileage(lower)
        vitals = self._extract_vitals(text)
        interventions = self._extract_interventions(lower)

        signature_present = any(
            phrase in lower
            for phrase in ["signature obtained", "signed transport paperwork", "representative signature"]
        )
        signature_exception = ""
        if "unable to sign" in lower:
            signature_exception = "Patient unable to sign due to documented condition."
        elif "refused signature" in lower:
            signature_exception = "Patient refused signature; refusal was witnessed."
        elif "no patient signature" in lower or "no signature" in lower:
            signature_exception = ""

        incident_type = "Non-emergency transport" if self._is_non_emergency(lower) else "Emergency transport"

        return PCRFields(
            chief_complaint=self._chief_complaint(lower),
            incident_type=incident_type,
            pickup_location=self._pickup_location(lower),
            destination=self._destination(text),
            vitals=vitals,
            interventions=interventions,
            mileage=mileage,
            medical_necessity=self._medical_necessity(lower, interventions, vitals),
            signature_present=signature_present,
            signature_exception=signature_exception,
            payer_type=self._payer_type(lower, incident_type),
            crew_notes=self._crew_notes(lower),
        )

    def warnings(self, fields: PCRFields) -> list[str]:
        warnings: list[str] = []
        if not fields.medical_necessity:
            warnings.append("Medical necessity narrative was not clearly detected.")
        if fields.mileage is None:
            warnings.append("Loaded mileage was not detected.")
        if not fields.signature_present and not fields.signature_exception:
            warnings.append("Signature or valid signature exception is missing.")
        return warnings

    def _extract_mileage(self, lower: str) -> float | None:
        patterns = [
            r"loaded mileage (?:was )?(\d+(?:\.\d+)?)",
            r"mileage was (\d+(?:\.\d+)?)",
            r"mileage (\d+(?:\.\d+)?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, lower)
            if match:
                return float(match.group(1))
        return None

    def _extract_vitals(self, text: str) -> list[str]:
        vitals: list[str] = []
        for pattern in [
            r"oxygen saturation of \d+ percent",
            r"blood pressure \d+ over \d+",
            r"pulse \d+",
            r"respirations \d+",
        ]:
            vitals.extend(match.group(0) for match in re.finditer(pattern, text, re.IGNORECASE))
        return vitals

    def _extract_interventions(self, lower: str) -> list[str]:
        options = [
            ("oxygen", "Oxygen by nasal cannula"),
            ("cardiac monitor", "Cardiac monitoring"),
            ("aspirin", "Aspirin per protocol"),
            ("spinal motion precautions", "Spinal motion precautions"),
            ("monitoring", "Crew monitoring during transport"),
            ("stretcher", "Stretcher transport"),
        ]
        interventions: list[str] = []
        for needle, label in options:
            if needle in lower and label not in interventions:
                interventions.append(label)
        return interventions

    def _is_non_emergency(self, lower: str) -> bool:
        return any(term in lower for term in ["non-emergency", "dialysis", "scheduled"])

    def _chief_complaint(self, lower: str) -> str:
        if "shortness of breath" in lower and "chest" in lower:
            return "Shortness of breath and chest discomfort"
        if "chest pain" in lower:
            return "Chest pain"
        if "fall" in lower and "hip pain" in lower:
            return "Fall with severe hip pain"
        if "dialysis" in lower:
            return "Scheduled dialysis transport"
        if "behavioral health" in lower or "confused" in lower:
            return "Behavioral health evaluation with altered mentation"
        return "Ambulance transport"

    def _pickup_location(self, lower: str) -> str:
        locations = [
            ("assisted living", "Assisted living facility"),
            ("urgent care", "Urgent care clinic"),
            ("community clinic", "Community clinic"),
            ("skilled nursing", "Skilled nursing facility"),
            ("from home", "Patient home"),
            (" at home", "Patient home"),
        ]
        for needle, label in locations:
            if needle in lower:
                return label
        return "Scene location not specified"

    def _destination(self, text: str) -> str:
        patterns = [
            r"transported(?: patient)?(?: emergent)? to ([A-Z][A-Za-z ]+(?:Center|Hospital|Clinic))",
            r"from home to ([A-Z][A-Za-z ]+(?:Center|Hospital|Clinic))",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "Destination not specified"

    def _medical_necessity(self, lower: str, interventions: list[str], vitals: list[str]) -> str:
        if "medical necessity narrative noted" in lower:
            return "Altered mentation and need for supervised ambulance transport."
        if "could not safely sit upright" in lower:
            return "Patient could not safely sit upright and required stretcher transport."
        if "oxygen saturation" in lower or "dyspnea" in lower:
            return "Abnormal oxygen saturation and dyspnea requiring monitoring and oxygen support."
        if "chest pain" in lower and ("cardiac monitor" in lower or "diaphoresis" in lower):
            return "Chest pain with abnormal findings requiring monitoring during transport."
        if "inability to stand" in lower:
            return "Severe pain and inability to stand requiring stretcher ambulance transport."
        if interventions or vitals:
            return "Crew assessment and transport monitoring supported ambulance medical necessity."
        return ""

    def _payer_type(self, lower: str, incident_type: str) -> str:
        if "dialysis" in lower:
            return "Medicaid"
        if incident_type == "Emergency transport":
            return "Medicare Advantage"
        return "Commercial"

    def _crew_notes(self, lower: str) -> str:
        notes: list[str] = []
        if "monitoring" in lower:
            notes.append("Crew monitoring documented.")
        if "unable to sign" in lower or "refused signature" in lower:
            notes.append("Signature exception narrative detected.")
        if "no patient signature" in lower or "no signature" in lower:
            notes.append("Signature is missing from the PCR narrative.")
        return " ".join(notes)
