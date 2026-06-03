import { RefreshCw, ShieldCheck } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Claim, ValidationResult, api } from '../api/client';
import ClaimCard from '../components/ClaimCard';
import ValidationPanel from '../components/ValidationPanel';

export default function ClaimsQueue() {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    setError('');
    try {
      const items = await api.claims();
      setClaims(items);
      if (!selectedId && items[0]) setSelectedId(items[0].id);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function validateSelected() {
    if (!selectedId) return;
    setLoading(true);
    setError('');
    try {
      setValidation(await api.validateClaim(selectedId));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  const selectedClaim = claims.find((claim) => claim.id === selectedId);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span>Pre-bill validation</span>
          <h1>Claims queue</h1>
        </div>
        <button className="icon-button" onClick={refresh} type="button" title="Refresh claims">
          <RefreshCw size={18} />
        </button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <section className="workspace-grid">
        <div className="list-panel">
          {claims.map((claim) => (
            <ClaimCard
              key={claim.id}
              claim={claim}
              selected={claim.id === selectedId}
              onSelect={() => {
                setSelectedId(claim.id);
                setValidation(null);
              }}
            />
          ))}
        </div>

        <div className="panel">
          <div className="section-heading">
            <div>
              <span>Selected claim</span>
              <h2>{selectedClaim?.id ?? 'No claim selected'}</h2>
            </div>
            <button className="primary-button" onClick={validateSelected} disabled={!selectedId || loading} type="button">
              <ShieldCheck size={17} /> Validate
            </button>
          </div>

          {selectedClaim ? (
            <div className="claim-detail-grid">
              <div>
                <span>Payer</span>
                <strong>{selectedClaim.payer}</strong>
              </div>
              <div>
                <span>Code</span>
                <strong>{selectedClaim.hcpcs_code}</strong>
              </div>
              <div>
                <span>Route</span>
                <strong>
                  {selectedClaim.pickup_location} to {selectedClaim.destination}
                </strong>
              </div>
              <div>
                <span>Medical necessity</span>
                <strong>{selectedClaim.medical_necessity || 'Missing'}</strong>
              </div>
            </div>
          ) : (
            <p className="muted-text">No claims loaded.</p>
          )}
        </div>
      </section>

      <ValidationPanel result={validation} />
    </div>
  );
}
