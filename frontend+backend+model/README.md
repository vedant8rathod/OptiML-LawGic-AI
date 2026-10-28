# AI Legal Assistant Module (Web-Ready)

Two features:
- Legal Research Tool (RAG over local judgments + Gemini summarization)
- Contract Analysis & Compliance Checker (clause-level risk + rewrite)

## Setup

1) Python 3.10+
2) Install requirements

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip; pip install -r requirements.txt
```

3) Environment variables (create .env):

```
GOOGLE_API_KEY=your_google_api_key
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/yourdb
PGVECTOR_TABLE=legal_embeddings
PGVECTOR_DIM=768
SPACY_MODEL=en_core_web_sm
DOCUMENTS_DIR=./documents
```

4) Install spaCy model if needed:

```powershell
python -m spacy download en_core_web_sm
```

## Index local documents

Place judgments under `./documents` (supports .txt, .pdf, .docx).

```powershell
python -c "from ai_legal_assistant.core.indexer import index_local_documents; print(index_local_documents())"
```

## Run example FastAPI server

```powershell
uvicorn examples.api_fastapi:app --reload
```

## API Examples

- POST /index → indexes documents
- POST /research {"query":"doctrine of promissory estoppel in India"}
- POST /contract {"text":"This Agreement allows unilateral termination without notice..."}

## Notes

- Ensure PostgreSQL has `pgvector` extension installed (`CREATE EXTENSION IF NOT EXISTS vector;`).
- The module keeps initialization separate for DB and embeddings to integrate with web backends.
- Gemini calls require a valid Google API key.
