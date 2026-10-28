# AI Legal Assistant – Session Notes (2025-10-11)

## Summary
- Implemented a web-ready Python module for two features:
  - Legal Research (spaCy + LangChain PGVector retriever + Gemini summarization)
  - Contract Analysis (clause segmentation + Gemini risk/rewrite/explanation)
- Added example FastAPI app exposing endpoints to index, research, and analyze contracts.
- Provided offline simulation helpers for deterministic sample outputs without external services.

## Key Files
- `ai_legal_assistant/` package with:
  - `core/` (config, NER, DB, embeddings, vectorstore, indexer)
  - `research.py` (legal research: sync+async)
  - `contract.py` (contract analysis: sync+async)
  - `samples.py` (offline sample outputs)
- `examples/api_fastapi.py` (FastAPI endpoints)
- `requirements.txt` and `README.md`

## Environment
- Python 3.10+
- PostgreSQL with `pgvector` extension
- Google Gemini API key (GOOGLE_API_KEY)

`.env` keys:
```
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/yourdb
PGVECTOR_TABLE=legal_embeddings
PGVECTOR_DIM=768
SPACY_MODEL=en_core_web_sm
DOCUMENTS_DIR=./documents
```

## Sample Outputs (offline simulation)
These were generated via:
```powershell
python -c "from ai_legal_assistant.samples import simulate_legal_research_output, simulate_contract_analysis_output; import json; print(json.dumps({'research': simulate_legal_research_output(), 'contract': simulate_contract_analysis_output()}, indent=2))"
```

### Research
```json
{
  "summary": "Based on the retrieved materials, the doctrine of promissory estoppel prevents a party from going back on clear promises when the other party has relied upon them to their detriment. The cases indicate courts assess clarity of representation, reliance, and equities.",
  "key_cases": [
    "Motilal Padampat Sugar Mills Co. Ltd. v. State of Uttar Pradesh",
    "Union of India v. Anglo Afghan Agencies",
    "Delhi Cloth & General Mills Co. Ltd. v. Union of India"
  ],
  "timeline": [
    {
      "date": "1962-12-05",
      "event": "Promissory estoppel recognized in export promotion scheme",
      "case_id": "UOI v. Anglo Afghan Agencies"
    },
    {
      "date": "1979-12-13",
      "event": "Expanded equitable application in fiscal matters",
      "case_id": "Motilal Padampat"
    }
  ]
}
```

### Contract Analysis
```json
[
  {
    "clause": "The Supplier may terminate this Agreement at any time without prior notice.",
    "risk": "High",
    "rewrite": "The Supplier may terminate this Agreement for convenience upon thirty (30) days' prior written notice. This clause does not limit either party's right to terminate for cause, including material breach.",
    "explanation": "Unconditional termination without notice is high risk due to fairness and potential unconscionability. Introducing a notice period and preserving for-cause rights reduces risk while maintaining flexibility."
  },
  {
    "clause": "All disputes shall be resolved exclusively in Supplier's home jurisdiction.",
    "risk": "Medium",
    "rewrite": "All disputes shall be resolved in the courts of [Mutually Agreed Jurisdiction], subject to mandatory consumer protection or employment laws, if applicable.",
    "explanation": "Exclusive jurisdiction heavily favoring one party can be unreasonable; offering a mutually agreed forum and acknowledging mandatory laws improves enforceability."
  }
]
```

## How to Resume

1) Activate env and install deps
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2) Index documents
```powershell
python -c "from ai_legal_assistant.core.indexer import index_local_documents; print(index_local_documents())"
```

3) Run API server
```powershell
uvicorn examples.api_fastapi:app --reload
```

4) Try endpoints
- POST /index
- POST /research  {"query":"doctrine of promissory estoppel in India","k":3}
- POST /contract  {"text":"This Agreement allows unilateral termination without notice..."}

## Next Steps
- Add tests for clause splitting and JSON parsing fallbacks
- Optionally switch to a legal-specific spaCy model for better NER
- Add Pydantic response models to FastAPI endpoints
