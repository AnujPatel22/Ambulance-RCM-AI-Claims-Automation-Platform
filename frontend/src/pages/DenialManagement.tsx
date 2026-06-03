import { FileText, RefreshCw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { AppealResponse, Denial, api } from '../api/client';
import AppealPreview from '../components/AppealPreview';
import DenialCard from '../components/DenialCard';

export default function DenialManagement() {
  const [denials, setDenials] = useState<Denial[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [selectedDenial, setSelectedDenial] = useState<Denial | null>(null);
  const [appeal, setAppeal] = useState<AppealResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    setError('');
    try {
      const items = await api.denials();
      setDenials(items);
      const first = items[0];
      if (first) {
        await selectDenial(first.id);
      }
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function selectDenial(id: string) {
    setSelectedId(id);
    setAppeal(null);
    setError('');
    try {
      setSelectedDenial(await api.denial(id));
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function generateAppeal() {
    if (!selectedId) return;
    setLoading(true);
    setError('');
    try {
      setAppeal(await api.generateAppeal(selectedId));
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
          <span>Denial management</span>
          <h1>Appeals workbench</h1>
        </div>
        <button className="icon-button" onClick={refresh} type="button" title="Refresh denials">
          <RefreshCw size={18} />
        </button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <section className="workspace-grid">
        <div className="list-panel">
          {denials.map((denial) => (
            <DenialCard
              key={denial.id}
              denial={denial}
              selected={denial.id === selectedId}
              onSelect={() => selectDenial(denial.id)}
            />
          ))}
        </div>

        <div className="panel">
          <div className="section-heading">
            <div>
              <span>Selected denial</span>
              <h2>{selectedDenial?.id ?? 'No denial selected'}</h2>
            </div>
            <button className="primary-button" onClick={generateAppeal} disabled={!selectedId || loading} type="button">
              <FileText size={17} /> Generate appeal
            </button>
          </div>

          {selectedDenial ? (
            <div className="claim-detail-grid">
              <div>
                <span>Claim</span>
                <strong>{selectedDenial.claim_id}</strong>
              </div>
              <div>
                <span>Payer</span>
                <strong>{selectedDenial.payer}</strong>
              </div>
              <div>
                <span>Reason</span>
                <strong>{selectedDenial.reason}</strong>
              </div>
              <div>
                <span>Missing evidence</span>
                <strong>{selectedDenial.missing_evidence.join(', ')}</strong>
              </div>
            </div>
          ) : (
            <p className="muted-text">No denials loaded.</p>
          )}
        </div>
      </section>

      <AppealPreview appeal={appeal} />
    </div>
  );
}
