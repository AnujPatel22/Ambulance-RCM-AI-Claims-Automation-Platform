import { ClipboardCheck, DollarSign, MapPin } from 'lucide-react';
import { Claim } from '../api/client';

type ClaimCardProps = {
  claim: Claim;
  selected: boolean;
  onSelect: () => void;
};

export default function ClaimCard({ claim, selected, onSelect }: ClaimCardProps) {
  return (
    <button className={selected ? 'item-card selected' : 'item-card'} onClick={onSelect} type="button">
      <div className="item-card-header">
        <strong>{claim.id}</strong>
        <span className={`status-pill ${claim.status}`}>{claim.status}</span>
      </div>
      <p>{claim.patient_label}</p>
      <div className="mini-row">
        <span>
          <ClipboardCheck size={14} /> {claim.hcpcs_code}
        </span>
        <span>
          <DollarSign size={14} /> {claim.billed_amount.toFixed(0)}
        </span>
      </div>
      <div className="mini-row">
        <span>
          <MapPin size={14} /> {claim.pickup_location || 'Missing origin'}
        </span>
      </div>
    </button>
  );
}
