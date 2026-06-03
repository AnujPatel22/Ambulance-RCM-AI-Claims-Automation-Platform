import { FileText } from 'lucide-react';
import { AppealResponse } from '../api/client';

type AppealPreviewProps = {
  appeal: AppealResponse | null;
};

export default function AppealPreview({ appeal }: AppealPreviewProps) {
  if (!appeal) {
    return (
      <section className="panel empty-panel">
        <FileText size={22} />
        <p>Select a denial and generate an appeal letter.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <span>Appeal preview</span>
          <h2>{appeal.appeal_id}</h2>
        </div>
        <span className="status-pill">{appeal.llm_provider} LLM</span>
      </div>
      <pre className="letter-preview">{appeal.letter_text}</pre>
      <div className="citation-row">
        {appeal.cited_rules.map((rule) => (
          <span key={rule.id}>{rule.id}</span>
        ))}
      </div>
    </section>
  );
}
