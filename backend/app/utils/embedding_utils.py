import os
import numpy as np

# Embedding utility with support for modern google-genai and fallback
genai_client = None
legacy_genai = None

try:
    from google import genai
    GENAI_MODERN = True
except ImportError:
    genai = None
    GENAI_MODERN = False
    try:
        import google.generativeai as legacy_genai
    except ImportError:
        legacy_genai = None


GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY") or "").strip()
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL") or "text-embedding-004"

if GEMINI_API_KEY:
    if GENAI_MODERN and genai is not None:
        try:
            genai_client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as exc:
            genai_client = None
            print(f"WARNING: Modern Gemini embedding client failed: {exc}")
    elif legacy_genai is not None:
        try:
            legacy_genai.configure(api_key=GEMINI_API_KEY)
        except Exception as exc:
            print(f"WARNING: Legacy Gemini embedding client failed: {exc}")
    else:
        print("WARNING: Gemini SDK not available for embeddings. Using deterministic fallback embeddings.")
else:
    print("INFO: Set GEMINI_API_KEY or AI_API_KEY to enable live embeddings")

async def get_embedding(text: str) -> list:
    """
    Returns vector embedding for a given text.
    Falls back to deterministic embeddings if Gemini API is not available.
    """
    if not GEMINI_API_KEY or (genai_client is None and legacy_genai is None):
        # Deterministic embedding based on hash
        np.random.seed(hash(text) % (2**32))
        return np.random.random(768).tolist()
    
    try:
        if genai_client is not None:
            # Modern google-genai client
            result = genai_client.models.embed_content(
                model=GEMINI_EMBED_MODEL,
                contents=text,
            )
            # Modern SDK returns EmbedContentResponse with embeddings list
            if hasattr(result, "embeddings") and result.embeddings:
                values = result.embeddings[0].values
                if values:
                    return list(values)
            if hasattr(result, "embedding") and result.embedding:
                values = result.embedding.values if hasattr(result.embedding, "values") else result.embedding
                return list(values)
        elif legacy_genai is not None:
            # Legacy SDK
            embedding = legacy_genai.embed_content(
                model=GEMINI_EMBED_MODEL,
                content=text,
            )
            data = embedding.get("embedding")
            if data:
                return data

        raise ValueError("Embedding response format unrecognized")
    except Exception as exc:
        print(f"WARNING: Embedding generation failed ({exc}); falling back to deterministic vector.")
        np.random.seed(hash(text) % (2**32))
        return np.random.random(768).tolist()

