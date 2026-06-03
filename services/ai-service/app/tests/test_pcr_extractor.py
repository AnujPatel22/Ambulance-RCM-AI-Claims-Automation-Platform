from app.services.pcr_extractor import PCRExtractor


def test_extracts_respiratory_transport_fields() -> None:
    transcript = (
        "Unit Medic 12 responded to a 74-year-old female with shortness of breath and chest "
        "discomfort at home. Patient had oxygen saturation of 88 percent on room air. Crew "
        "administered oxygen by nasal cannula and transported patient to Valley Medical Center. "
        "Mileage was 12.4 miles. Patient was unable to sign due to respiratory distress."
    )

    result = PCRExtractor().extract(transcript)

    assert result.chief_complaint == "Shortness of breath and chest discomfort"
    assert result.mileage == 12.4
    assert result.destination == "Valley Medical Center"
    assert "Oxygen by nasal cannula" in result.interventions
    assert result.signature_exception


def test_missing_signature_warning() -> None:
    extractor = PCRExtractor()
    fields = extractor.extract(
        "Ambulance 7 completed a non-emergency dialysis transport from home to River Dialysis "
        "Center. Mileage was 4.1 miles. No patient signature or signature exception was documented."
    )

    assert "Signature or valid signature exception is missing." in extractor.warnings(fields)
