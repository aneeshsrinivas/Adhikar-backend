# scripts/seed_vectorstore.py

import sys
import os
sys.path.append(os.getcwd())

from app.firebase import db
from app.ai.embeddings import embed_texts
from app.ai.vectorstore import upsert_documents

print("🔥 Fetching schemes from Firestore...")

docs = db.collection("schemes").stream()
schemes = [d.to_dict() for d in docs]

if not schemes:
    print("❌ No schemes found in Firestore.")
    exit()

ids = []
metadatas = []
texts = []

for s in schemes:
    sid = s.get("id") or s.get("name")
    ids.append(sid)

    combined_text = f"""
    Name: {s.get('name')}
    Category: {s.get('category')}
    Eligibility: {s.get('eligibility')}
    Benefits: {s.get('benefits')}
    State: {s.get('state')}
    """

    texts.append(combined_text)

    metadatas.append({
        "name": s.get("name"),
        "category": s.get("category"),
        "eligibility": s.get("eligibility"),
        "benefits": s.get("benefits"),
        "state": s.get("state"),
        "apply_link": s.get("apply_link")
    })

print("🧠 Generating embeddings...")
embeddings = embed_texts(texts)

print("💾 Storing embeddings into ChromaDB...")
upsert_documents(ids, metadatas, embeddings)

print("🎉 Vectorstore seeding completed successfully!")
