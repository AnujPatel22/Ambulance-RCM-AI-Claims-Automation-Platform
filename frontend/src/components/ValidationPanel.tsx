import { CheckCircle2, CircleAlert, Wrench } from 'lucide-react';
import { ValidationResult } from '../api/client';

type ValidationPanelProps = {
  result: ValidationResult | null;
};

export default function ValidationPanel({ result }: ValidationPanelProps) {
  if (!result) {
    return (
      <section className="panel empty-panel">
        <CircleAlert size={22} />
        <p>Select a claim and run validation.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <span>Validation result</span>
          <h2>{result.claim_id}</h2>
        </div>
        <span className={`risk-badge ${result.denial_risk_level.toLowerCase()}`}>
          {result.denial_risk_level} risk
        </span>
      </div>

      <div className="score-bar" aria-label="Denial risk score">
        <span style={{ width: `${Math.round(result.denial_risk_score * 100)}%` }} />
      </div>

      <div className="two-column">
        <div>
          <h3>
            <CircleAlert size={16} /> Missing requirements
          </h3>
          <ul className="check-list">
            {result.missing_requirements.length === 0 ? (
              <li>
                <CheckCircle2 size={15} /> No missing requirements detected.
              </li>
            ) : (
              result.missing_requirements.map((item) => (
                <li key={item}>
                  <CircleAlert size={15} /> {item}
                </li>
              ))
            )}
          </ul>
        </div>
        <div>
          <h3>
            <Wrench size={16} /> Recommended fixes
          </h3>
          <ul className="check-list">
            {result.recommended_fixes.map((item) => (
              <li key={item}>
                <Wrench size={15} /> {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
