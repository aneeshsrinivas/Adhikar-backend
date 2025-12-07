# app/ai/vectorstore.py

from chromadb import PersistentClient
from typing import List, Dict, Any
import os

PERSIST_DIR = "data/chroma"
COLLECTION_NAME = "schemes_vectorstore"

_client = None
_collection = None


# ------------------------------------------
# Create persistent client (correct for new Chroma)
# ------------------------------------------
def get_client():
    global _client
    if _client is None:
        os.makedirs(PERSIST_DIR, exist_ok=True)
        _client = PersistentClient(path=PERSIST_DIR)
    return _client


# ------------------------------------------
# Get or create collection
# ------------------------------------------
def get_collection():
    global _collection
    client = get_client()

    try:
        _collection = client.get_collection(COLLECTION_NAME)
    except:
        _collection = client.create_collection(name=COLLECTION_NAME)

    return _collection


# ------------------------------------------
# Helper: clean metadata (remove None)
# ------------------------------------------
def clean_metadata(meta: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    for k, v in meta.items():
        if v is None:
            cleaned[k] = ""      # Replace None with empty string
        else:
            cleaned[k] = v
    return cleaned


# ------------------------------------------
# Upsert documents safely
# ------------------------------------------
def upsert_documents(ids: List[str], metadatas: List[Dict], embeddings: List[List[float]]):
    col = get_collection()

    # CLEAN metadata for Chroma (NO None allowed)
    cleaned_metas = [clean_metadata(m) for m in metadatas]

    col.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=cleaned_metas
    )

    print(f"✅ Upserted {len(ids)} items into ChromaDB.")


# ------------------------------------------
# Query similar documents
# ------------------------------------------
def query(query_embedding: List[float], top_k: int = 5):
    col = get_collection()

    results = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
