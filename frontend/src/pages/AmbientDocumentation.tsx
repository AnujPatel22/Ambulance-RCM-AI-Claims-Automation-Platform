import { ClipboardPlus, FilePlus2, Wand2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Claim, PCRExtractionResponse, PCRSample, ValidationResult, api } from '../api/client';
import ValidationPanel from '../components/ValidationPanel';

export default function AmbientDocumentation() {
  const [samples, setSamples] = useState<PCRSample[]>([]);
  const [transcript, setTranscript] = useState('');
  const [selectedSampleId, setSelectedSampleId] = useState('');
  const [extraction, setExtraction] = useState<PCRExtractionResponse | null>(null);
  const [createdClaim, setCreatedClaim] = useState<Claim | null>(null);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api
      .samples()
      .then((items) => {
        setSamples(items);
        if (items[0]) {
          setSelectedSampleId(items[0].id);
          setTranscript(items[0].transcript);
        }
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  function chooseSample(id: string) {
    const sample = samples.find((item) => item.id === id);
    setSelectedSampleId(id);
    if (sample) {
      setTranscript(sample.transcript);
      setExtraction(null);
      setCreatedClaim(null);
      setValidation(null);
    }
  }

  async function runExtraction() {
    setLoading(true);
    setError('');
    try {
      const result = await api.extract(transcript, true);
      setExtraction(result);
      setCreatedClaim(null);
      setValidation(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function createAndValidateClaim() {
    if (!extraction) return;
    setLoading(true);
    setError('');
    try {
      const fields = extraction.fields;
      const claim = await api.createClaim({
        pcr_id: extraction.pcr_id ?? undefined,
        patient_label: 'Synthetic Demo Patient',
        payer: fields.payer_type === 'Medicaid' ? 'State EMS Medicaid' : 'Metro Medicare Advantage',
        payer_type: fields.payer_type || 'Medicare Advantage',
        hcpcs_code: fields.incident_type.includes('Non') ? 'A0428' : 'A0427',
        incident_type: fields.incident_type,
        pickup_location: fields.pickup_location,
        destination: fields.destination,
        mileage: fields.mileage,
        medical_necessity: fields.medical_necessity,
        signature_present: fields.signature_present,
        signature_exception: fields.signature_exception,
        status: 'prebill',
        billed_amount: 950
      });
      setCreatedClaim(claim);
      setValidation(await api.validateClaim(claim.id));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span>Ambient EMS documentation</span>
          <h1>Transcript to structured PCR fields</h1>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <section className="workspace-grid">
        <div className="panel">
          <div className="section-heading">
            <div>
              <span>Synthetic narrative</span>
              <h2>EMS transcript</h2>
            </div>
            <select value={selectedSampleId} onChange={(event) => chooseSample(event.target.value)}>
              {samples.map((sample) => (
                <option key={sample.id} value={sample.id}>
                  {sample.title}
                </option>
              ))}
            </select>
          </div>

          <textarea
            value={transcript}
            onChange={(event) => setTranscript(event.target.value)}
            rows={13}
            aria-label="Synthetic EMS transcript"
          />

          <div className="button-row">
            <button className="primary-button" onClick={runExtraction} disabled={loading || !transcript} type="button">
              <Wand2 size={17} /> Extract PCR fields
            </button>
            <button
              className="secondary-button"
              onClick={createAndValidateClaim}
              disabled={loading || !extraction}
              type="button"
            >
              <FilePlus2 size={17} /> Create and validate claim
            </button>
          </div>
        </div>

        <div className="panel">
          <div className="section-heading">
            <div>
              <span>Auto-populated PCR</span>
              <h2>Structured fields</h2>
            </div>
            <ClipboardPlus size={24} />
          </div>

          {!extraction && <p className="muted-text">Run extraction to populate PCR fields.</p>}
          {extraction && (
            <div className="field-grid">
              {Object.entries(extraction.fields).map(([key, value]) => (
                <div key={key} className="field-row">
                  <span>{key.replaceAll('_', ' ')}</span>
                  <strong>{Array.isArray(value) ? value.join(', ') || 'None' : String(value ?? 'Not detected')}</strong>
                </div>
              ))}
              {extraction.warnings.map((warning) => (
                <div key={warning} className="warning-chip">
                  {warning}
                </div>
              ))}
            </div>
          )}

          {createdClaim && (
            <div className="created-claim">
              <span>Created claim</span>
              <strong>{createdClaim.id}</strong>
            </div>
          )}
        </div>
      </section>

      <ValidationPanel result={validation} />
    </div>
  );
}
