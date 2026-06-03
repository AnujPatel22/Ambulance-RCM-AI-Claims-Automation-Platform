import { Search } from 'lucide-react';
import { useState } from 'react';
import { PayerRule, api } from '../api/client';

export default function RulesExplorer() {
  const [payer, setPayer] = useState('Metro Medicare Advantage');
  const [code, setCode] = useState('A0427');
  const [reason, setReason] = useState('Medical necessity insufficient');
  const [query, setQuery] = useState('oxygen abnormal vitals monitoring');
  const [rules, setRules] = useState<PayerRule[]>([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function search() {
    setLoading(true);
    setError('');
    try {
      const result = await api.searchRules({
        payer,
        hcpcs_code: code,
        denial_reason: reason,
        query,
        limit: 6
      });
      setRules(result.rules);
      setSummary(result.query_summary);
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
          <span>Payer rule retrieval</span>
          <h1>Rules explorer</h1>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <section className="panel">
        <div className="search-grid">
          <label>
            Payer
            <select value={payer} onChange={(event) => setPayer(event.target.value)}>
              <option>Metro Medicare Advantage</option>
              <option>State EMS Medicaid</option>
              <option>Southwest Commercial Health</option>
              <option>Self Pay Demo Plan</option>
            </select>
          </label>
          <label>
            HCPCS
            <select value={code} onChange={(event) => setCode(event.target.value)}>
              <option>A0427</option>
              <option>A0428</option>
              <option>A0429</option>
              <option>ALL</option>
            </select>
          </label>
          <label>
            Denial reason
            <input value={reason} onChange={(event) => setReason(event.target.value)} />
          </label>
          <label>
            Keywords
            <input value={query} onChange={(event) => setQuery(event.target.value)} />
          </label>
        </div>
        <button className="primary-button" onClick={search} disabled={loading} type="button">
          <Search size={17} /> Search rules
        </button>
      </section>

      <section className="rules-list">
        {summary && <p className="muted-text">Retrieved for: {summary}</p>}
        {rules.map((rule) => (
          <article className="rule-card" key={rule.id}>
            <div className="item-card-header">
              <strong>{rule.title}</strong>
              <span className="status-pill">{rule.id}</span>
            </div>
            <p>{rule.rule_text}</p>
            <div className="citation-row">
              <span>{rule.payer}</span>
              <span>{rule.hcpcs_code}</span>
              <span>score {rule.score ?? 0}</span>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}
