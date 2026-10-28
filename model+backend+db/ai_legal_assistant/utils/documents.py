from __future__ import annotations

import os
from typing import Iterable, List, Optional

from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.docstore.document import Document

from ..core.config import settings


def iter_document_paths(root: Optional[str] = None) -> Iterable[str]:
    root = root or settings.documents_dir
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith((".txt", ".pdf", ".docx")):
                yield os.path.join(dirpath, name)


def load_document(path: str) -> List[Document]:
    lower = path.lower()
    if lower.endswith(".txt"):
        return TextLoader(path, autodetect_encoding=True).load()
    if lower.endswith(".pdf"):
        return PyPDFLoader(path).load()
    if lower.endswith(".docx"):
        return UnstructuredWordDocumentLoader(path).load()
    raise ValueError(f"Unsupported file type: {path}")


def load_all_documents(root: Optional[str] = None) -> List[Document]:
    docs: List[Document] = []
    for p in iter_document_paths(root):
        try:
            docs.extend(load_document(p))
        except Exception:
            # Skip files that fail to parse; in production log the error
            continue
    return docs
