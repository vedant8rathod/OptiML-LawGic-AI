# LawGic AI ⚖️

A full-stack web application designed to simplify legal documents and questions. It combines an interactive chat assistant (powered by Google Gemini with a rule-based offline fallback) with a specialized **Legal Entity Intelligence** engine built for Indian legal contexts (court judgments, contracts, petitions, and notices).

---

## What It Does

- **Legal Query Assistant (`/ask-ai`)**:
  - Ask legal questions in plain English or Hindi.
  - Upload supporting files (`.pdf`, `.docx`, `.txt`) or voice notes (`.mp3`, `.wav`, `.m4a`).
  - Choose between Quick Answers (`/api/predict/`), Comprehensive Document Analysis (`/api/analyze/`), or In-Depth Research with Indian case law citations (`/api/research/`).
  
- **Legal Entity Intelligence (`/entities`)**:
  - **Named Entity Recognition (NER)**: Identifies 16 entity types tailored for the Indian legal system, including Courts (Supreme Court, High Courts, Tribunals), Statutes (IPC, CrPC, NI Act, etc.), Sections/Articles, Case Citation numbers, Parties, Judges, Advocates, and Indian currency formats (₹ / Lakhs / Crores).
  - **Smart Highlighter**: Highlights detected entities directly inside the document viewer without altering formatting or character offsets.
  - **Entity Explorer**: Groups entities into clean categories with mention counts and jump-to-text links.
  - **Relationship Extraction**: Detects connections like *Advocate representing Party*, *Court hearing Case*, *Party claiming Damages*, and *Section contained in Statute*.
  - **Case Timeline**: Extracts dates and milestones into an interactive chronological view.
  - **Privacy Redactor**: Automatically sanitizes sensitive PII (names, phone numbers, email addresses, financial amounts) before documents are exported.
  - **Export**: Download extracted entity data directly as CSV.

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, modern `google-genai` SDK.
- **NLP**: Custom regex & gazetteer-based legal pattern extraction, sentence-level relation extraction, coreference clustering.
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, Radix UI.

---

## Getting Started on Windows

### 1. Prerequisites
Make sure you have installed:
- [Python 3.10+](https://www.python.org/downloads/) (check "Add python.exe to PATH" during install)
- [Node.js (LTS version)](https://nodejs.org/)

---

### 2. Setting Up the Backend

Open PowerShell and run:

```powershell
# Navigate to the backend folder
cd backend

# Create and activate a Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Create the SQLite database tables
python init_db.py

# Start the FastAPI server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger API Docs: `http://127.0.0.1:8000/docs`

> **Note on Gemini API Key**: The app works out-of-the-box in offline fallback mode. If you want live Gemini responses, create a file named `.env` inside `backend/` and add:
> ```env
> GEMINI_API_KEY=your_gemini_api_key_here
> GEMINI_MODEL_NAME=gemini-2.5-flash
> ```

---

### 3. Setting Up the Frontend

Open a **new** PowerShell window and run:

```powershell
# Navigate to the frontend folder
cd frontend

# Install JavaScript dependencies
npm install

# Start the Vite development server
npm run dev
```

- Web App: open [http://localhost:8080](http://localhost:8080) in your browser.

---

## Running Backend Tests

In your backend terminal (with the virtual environment active):

```powershell
# Run the test suite
pytest tests/test_nlp_entities.py -v

# Run the benchmark evaluation
python tests/eval_benchmark.py
```

---

## Project Structure

```
OptiML-LawGic-AI/
├── backend/
│   ├── app/
│   │   ├── db/                 # Database models and SQLite setup
│   │   ├── ml/                 # Rule-based offline legal model
│   │   ├── nlp/                # Legal Entity Intelligence pipeline
│   │   │   ├── ner_engine.py          # Entity recognition (16 types)
│   │   │   ├── legal_patterns.py      # Indian legal pattern definitions
│   │   │   ├── relation_extractor.py  # Relationship extraction
│   │   │   ├── timeline_generator.py  # Chronological timeline builder
│   │   │   ├── privacy_redactor.py    # PII sanitization
│   │   │   └── entity_service.py      # Main NLP service orchestrator
│   │   ├── routes/             # Endpoints (predict, analyze, research, entities)
│   │   ├── utils/              # File parsing, model loader, embeddings
│   │   └── main.py             # FastAPI entrypoint
│   ├── tests/                  # Pytest test cases and NLP evaluation
│   ├── init_db.py              # Database initialization script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # UI components & legal entity views
│   │   ├── pages/              # Index, AskAI, LegalEntities
│   │   ├── services/api.ts     # Backend API client
│   │   └── App.tsx             # Routes & layout
│   └── package.json
└── README.md
```
