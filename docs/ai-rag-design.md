# AI and RAG Design

The MVP uses a reliable simple RAG design:

- Synthetic payer rules are stored in PostgreSQL.
- Queries filter by payer, HCPCS-style code, denial reason, and keywords.
- Results are scored with exact and keyword matches.
- Retrieved snippets are cited in validation and appeal generation.

The LLM client is provider-agnostic and defaults to a mock response. If `LLM_API_KEY` is absent or an upstream call fails, the app still produces deterministic extraction and appeal outputs.

This project intentionally avoids real policy documents and real PHI.
