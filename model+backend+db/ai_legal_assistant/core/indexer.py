from __future__ import annotations

from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import settings
from .vectorstore import get_vectorstore, ensure_table
from ..utils.documents import load_all_documents


def index_local_documents(root: Optional[str] = None, chunk_size: int = 1000, chunk_overlap: int = 150) -> int:
    """Load local judgments and index into pgvector store.

    Returns number of chunks added.
    """
    ensure_table()
    vs = get_vectorstore()

    docs = load_all_documents(root or settings.documents_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    if not chunks:
        return 0

    vs.add_documents(chunks)
    return len(chunks)
