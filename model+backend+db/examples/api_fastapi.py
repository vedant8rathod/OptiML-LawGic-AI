from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_legal_assistant.research import legal_research, legal_research_async
from ai_legal_assistant.contract import analyze_contract
from ai_legal_assistant.core.indexer import index_local_documents
from ai_legal_assistant.core.db import ensure_pgvector

app = FastAPI(title="AI Legal Assistant")


class ResearchRequest(BaseModel):
    query: str
    k: int = 3


class ContractRequest(BaseModel):
    text: str


@app.on_event("startup")
async def startup_event():
    # Ensure pgvector extension exists if DB is configured
    try:
        ensure_pgvector()
    except Exception:
        pass


@app.post("/index")
async def index_documents() -> dict[str, Any]:
    try:
        n = index_local_documents()
        return {"indexed_chunks": n}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/research")
async def research(req: ResearchRequest) -> Any:
    try:
        return await legal_research_async(req.query, top_k=req.k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contract")
async def contract(req: ContractRequest) -> Any:
    try:
        return analyze_contract(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
