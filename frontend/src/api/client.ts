const AI_BASE_URL = import.meta.env.VITE_AI_SERVICE_URL ?? 'http://localhost:8000';
const CLAIMS_BASE_URL = import.meta.env.VITE_CLAIMS_SERVICE_URL ?? 'http://localhost:8080';

export type PCRFields = {
  chief_complaint: string;
  incident_type: string;
  pickup_location: string;
  destination: string;
  vitals: string[];
  interventions: string[];
  mileage: number | null;
  medical_necessity: string;
  signature_present: boolean;
  signature_exception: string;
  payer_type: string;
  crew_notes: string;
};

export type PCRSample = {
  id: string;
  title: string;
  transcript: string;
};

export type PCRExtractionResponse = {
  pcr_id: string | null;
  fields: PCRFields;
  warnings: string[];
};

export type Claim = {
  id: string;
  pcr_id?: string;
  patient_label: string;
  payer: string;
  payer_type: string;
  hcpcs_code: string;
  incident_type: string;
  pickup_location: string;
  destination: string;
  mileage: number | null;
  medical_necessity: string;
  signature_present: boolean;
  signature_exception: string;
  status: string;
  billed_amount: number;
  created_at?: string;
};

export type ClaimCreateRequest = Omit<Claim, 'id' | 'created_at'>;

export type ValidationResult = {
  claim_id: string;
  denial_risk_score: number;
  denial_risk_level: string;
  missing_requirements: string[];
  recommended_fixes: string[];
  cited_rule_ids: string[];
};

export type Denial = {
  id: string;
  claim_id: string;
  payer: string;
  reason: string;
  status: string;
  missing_evidence: string[];
  denial_date?: string;
  claim?: Claim;
};

export type PayerRule = {
  id: string;
  payer: string;
  payer_type: string;
  hcpcs_code: string;
  denial_reason: string;
  title: string;
  rule_text: string;
  required_fields: string[];
  keywords: string[];
  score?: number;
};

export type AppealResponse = {
  appeal_id: string;
  denial_id: string | null;
  claim_id: string | null;
  letter_text: string;
  cited_rules: PayerRule[];
  llm_provider: string;
};

export type AnalyticsSummary = {
  total_claims: number;
  total_denials: number;
  high_denial_risk_claims: number;
  missing_documentation_count: number;
  denial_rate_reduction_percent: number;
  risk_before_validation: number;
  risk_after_validation: number;
  manual_resolution_days: number;
  automated_resolution_days: number;
  appeals_generated: number;
};

export type RAGSearchResponse = {
  rules: PayerRule[];
  query_summary: string;
};

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {})
    }
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  analytics: () => request<AnalyticsSummary>(`${AI_BASE_URL}/analytics/summary`),
  samples: () => request<PCRSample[]>(`${AI_BASE_URL}/documentation/samples`),
  extract: (transcript: string, persist = true) =>
    request<PCRExtractionResponse>(`${AI_BASE_URL}/documentation/extract`, {
      method: 'POST',
      body: JSON.stringify({ transcript, persist })
    }),
  searchRules: (payload: {
    query?: string;
    payer?: string;
    hcpcs_code?: string;
    denial_reason?: string;
    keywords?: string[];
    limit?: number;
  }) =>
    request<RAGSearchResponse>(`${AI_BASE_URL}/rag/search`, {
      method: 'POST',
      body: JSON.stringify(payload)
    }),
  generateAppeal: (denialId: string) =>
    request<AppealResponse>(`${AI_BASE_URL}/appeals/generate`, {
      method: 'POST',
      body: JSON.stringify({ denial_id: denialId })
    }),
  claims: () => request<Claim[]>(`${CLAIMS_BASE_URL}/claims`),
  claim: (id: string) => request<Claim>(`${CLAIMS_BASE_URL}/claims/${id}`),
  createClaim: (payload: ClaimCreateRequest) =>
    request<Claim>(`${CLAIMS_BASE_URL}/claims`, {
      method: 'POST',
      body: JSON.stringify(payload)
    }),
  validateClaim: (id: string) =>
    request<ValidationResult>(`${CLAIMS_BASE_URL}/claims/${id}/validate`, {
      method: 'POST'
    }),
  denials: () => request<Denial[]>(`${CLAIMS_BASE_URL}/denials`),
  denial: (id: string) => request<Denial>(`${CLAIMS_BASE_URL}/denials/${id}`)
};
