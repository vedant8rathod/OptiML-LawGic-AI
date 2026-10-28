# AI Legal Assistant (Clean)

This is a cleaned project layout for the FastAPI-based AI Legal Assistant with Postgres + pgvector and Gemini.

## Structure
- backend/: FastAPI app code (app package), build_model.py helper, ai_legal_model convenience import
- docker/: Dockerfile
- data/: model and artifacts (e.g., models/model.pkl)
- tests/: integration tests (optional placeholder)
- docs/: this README and any other docs
- docker-compose.yml: Orchestrates db and backend services
- .env: Set GOOGLE_API_KEY and AI_LEGAL_USE_REAL=1

## Run
1. Set `.env` at project root:
   - GOOGLE_API_KEY=your-key
   - AI_LEGAL_USE_REAL=1
2. Build the model (optional if already present):
   - docker compose run --rm backend python build_model.py
3. Start services:
   - docker compose up -d --build
4. Check:
   - http://localhost:8000/health
   - http://localhost:8000/docs

## Endpoints
- POST /api/analyze/
- POST /api/research/

## Notes
- Embeddings use pgvector (Vector(768)); the raw vector is also stored in Document.embedding (JSON).
- If GOOGLE_API_KEY is missing, embeddings default to zeros and model predictions fall back to simulation.
