import { Activity, Clock, FileWarning, Gauge, TrendingDown } from 'lucide-react';
import { useEffect, useState } from 'react';
import { AnalyticsSummary, api } from '../api/client';
import MetricCard from '../components/MetricCard';

export default function Dashboard() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api
      .analytics()
      .then(setSummary)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <div>
          <span>Revenue-cycle command center</span>
          <h1>Ambulance RCM & AI Claims Automation</h1>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}
      {!summary && !error && <div className="loading-band">Loading synthetic operating metrics...</div>}

      {summary && (
        <>
          <section className="metric-grid">
            <MetricCard
              icon={<Activity size={21} />}
              label="Total claims"
              value={String(summary.total_claims)}
              helper={`${summary.total_denials} synthetic denials in queue`}
              tone="blue"
            />
            <MetricCard
              icon={<FileWarning size={21} />}
              label="High-risk claims"
              value={String(summary.high_denial_risk_claims)}
              helper={`${summary.missing_documentation_count} missing documentation items`}
              tone="red"
            />
            <MetricCard
              icon={<TrendingDown size={21} />}
              label="Denial reduction"
              value={`${summary.denial_rate_reduction_percent}%`}
              helper="Simulated after pre-bill validation"
              tone="green"
            />
            <MetricCard
              icon={<Clock size={21} />}
              label="Appeal cycle"
              value={`${summary.manual_resolution_days}d -> ${summary.automated_resolution_days}d`}
              helper={`${summary.appeals_generated} generated appeal letters stored`}
              tone="amber"
            />
          </section>

          <section className="panel">
            <div className="section-heading">
              <div>
                <span>Risk movement</span>
                <h2>Pre-bill validation impact</h2>
              </div>
              <Gauge size={24} />
            </div>
            <div className="risk-comparison">
              <div>
                <span>Before validation</span>
                <strong>{Math.round(summary.risk_before_validation * 100)}%</strong>
                <div className="score-bar muted">
                  <span style={{ width: `${summary.risk_before_validation * 100}%` }} />
                </div>
              </div>
              <div>
                <span>After validation</span>
                <strong>{Math.round(summary.risk_after_validation * 100)}%</strong>
                <div className="score-bar">
                  <span style={{ width: `${summary.risk_after_validation * 100}%` }} />
                </div>
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
