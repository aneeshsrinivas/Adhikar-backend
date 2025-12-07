# app/ai/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Load model only once (cached globally)
_MODEL = None

def load_model(name: str = "all-MiniLM-L6-v2"):
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(name)
    return _MODEL

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Returns L2-normalized embeddings for stable cosine similarity search.
    """
    model = load_model()
    embeddings = model.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True
    )

    # Normalize embeddings (recommended)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized = embeddings / norms

    return normalized.tolist()

def embed_one(text: str) -> List[float]:
    """Embed a single string for querying vectorstore."""
    return embed_texts([text])[0]
