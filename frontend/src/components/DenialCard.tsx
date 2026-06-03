import { AlertTriangle, CalendarDays } from 'lucide-react';
import { Denial } from '../api/client';

type DenialCardProps = {
  denial: Denial;
  selected: boolean;
  onSelect: () => void;
};

export default function DenialCard({ denial, selected, onSelect }: DenialCardProps) {
  return (
    <button className={selected ? 'item-card selected' : 'item-card'} onClick={onSelect} type="button">
      <div className="item-card-header">
        <strong>{denial.id}</strong>
        <span className={`status-pill ${denial.status}`}>{denial.status.replace('_', ' ')}</span>
      </div>
      <p>{denial.reason}</p>
      <div className="mini-row">
        <span>
          <AlertTriangle size={14} /> {denial.claim_id}
        </span>
        <span>
          <CalendarDays size={14} /> {denial.denial_date ?? 'Open'}
        </span>
      </div>
    </button>
  );
}
