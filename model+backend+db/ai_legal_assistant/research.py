from __future__ import annotations

from typing import List
import json

from .core.config import settings
from .core.ner import extract_entities
from .core.vectorstore import get_vectorstore
from .core.types import ResearchResult
from .core.gemini import ensure_gemini_configured


def _summarize_results_gemini(query: str, contexts: List[str]) -> ResearchResult:
    """Summarize retrieved contexts using Gemini into structured output.

    Note: This uses a synchronous call for simplicity. For web backends,
    wrap in an executor or use an async variant.
    """
    # Lazy import to avoid import-time errors if deps are missing
    ensure_gemini_configured()
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.google_api_key, temperature=0.2)
    prompt = (
        "You are a legal research assistant. Based on the user's query and the retrieved case excerpts, "
        "produce: (1) a concise summary (<=200 words), (2) a list of key case names, and (3) a simple timeline JSON array.\n\n"
        f"Query: {query}\n\n"
        f"Excerpts:\n- " + "\n- ".join(contexts) + "\n\n"
        "Return JSON with keys: summary (string), key_cases (array of strings), timeline (array of {date, event, case_id})."
    )
    res = llm.invoke(prompt)
    # Attempt to parse JSON from response
    text = res.content if hasattr(res, "content") else str(res)
    try:
        data = json.loads(text)
    except Exception:
        # Fallback: create minimal structure
        data = {
            "summary": text[:1000],
            "key_cases": [],
            "timeline": [],
        }
    return ResearchResult(**data)  # type: ignore[arg-type]


async def _summarize_results_gemini_async(query: str, contexts: List[str]) -> ResearchResult:
    ensure_gemini_configured()
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.google_api_key, temperature=0.2)
    prompt = (
        "You are a legal research assistant. Based on the user's query and the retrieved case excerpts, "
        "produce: (1) a concise summary (<=200 words), (2) a list of key case names, and (3) a simple timeline JSON array.\n\n"
        f"Query: {query}\n\n"
        f"Excerpts:\n- " + "\n- ".join(contexts) + "\n\n"
        "Return JSON with keys: summary (string), key_cases (array of strings), timeline (array of {date, event, case_id})."
    )
    res = await llm.ainvoke(prompt)
    text = res.content if hasattr(res, "content") else str(res)
    try:
        data = json.loads(text)
    except Exception:
        data = {"summary": text[:1000], "key_cases": [], "timeline": []}
    return ResearchResult(**data)  # type: ignore[arg-type]


def legal_research(query: str, top_k: int = 3) -> ResearchResult:
    """Run legal research over local embeddings and summarize with Gemini.

    Steps:
    1) spaCy extract entities from query (not strictly required but can be used for filters later)
    2) Query PGVector via LangChain retriever
    3) Summarize into structured JSON via Gemini
    """
    _ = extract_entities(query)

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    # We can use a simple RetrievalQA to get contexts, but we won't rely on the LLM answer; we will collect docs.
    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI
    ensure_gemini_configured()
    chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.google_api_key, temperature=0.1),
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

    result = chain.invoke({"query": query})
    docs = result.get("source_documents", [])
    contexts: List[str] = [d.page_content for d in docs]

    return _summarize_results_gemini(query, contexts)


async def legal_research_async(query: str, top_k: int = 3) -> ResearchResult:
    """Async variant of legal research using async Gemini calls."""
    _ = extract_entities(query)

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    from langchain.chains import RetrievalQA
    from langchain_google_genai import ChatGoogleGenerativeAI
    ensure_gemini_configured()
    chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.google_api_key, temperature=0.1),
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

    result = await chain.ainvoke({"query": query})
    docs = result.get("source_documents", [])
    contexts: List[str] = [d.page_content for d in docs]

    return await _summarize_results_gemini_async(query, contexts)
