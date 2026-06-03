import { ReactNode } from 'react';

type MetricCardProps = {
  label: string;
  value: string;
  helper: string;
  icon: ReactNode;
  tone?: 'blue' | 'green' | 'amber' | 'red';
};

export default function MetricCard({ label, value, helper, icon, tone = 'blue' }: MetricCardProps) {
  return (
    <article className={`metric-card ${tone}`}>
      <div className="metric-icon">{icon}</div>
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{helper}</p>
    </article>
  );
}
