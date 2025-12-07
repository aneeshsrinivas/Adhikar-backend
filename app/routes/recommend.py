# app/routes/recommend.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.ai.embeddings import embed_texts
from app.ai.vectorstore import query as vector_query
from app.ai.gemini_client import call_gemini
import json
import re

router = APIRouter(prefix="/api", tags=["AI Recommendation"])


# ---------------------------------------------------
# Request Model
# ---------------------------------------------------
class RecommendRequest(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[float] = None
    free_text: Optional[str] = None
    top_k: Optional[int] = 3


# ---------------------------------------------------
# Local Fallback (No Gemini)
# ---------------------------------------------------
def local_fallback(candidates: List[Dict], req: RecommendRequest, k=3):
    keywords = []

    if req.state: keywords.append(req.state.lower())
    if req.category: keywords.append(req.category.lower())
    if req.occupation: keywords.extend(req.occupation.lower().split())
    if req.free_text: keywords.extend(req.free_text.lower().split())

    scored = []

    for s in candidates:
        text = (
            f"{s.get('name', '')} "
            f"{s.get('category', '')} "
            f"{s.get('eligibility', '')} "
            f"{s.get('benefits', '')}"
        ).lower()

        score = sum(text.count(w) for w in keywords)
        scored.append((score, s))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [
        {
            "name": s.get("name"),
            "why_fit": f"Matched keywords (score={score})",
            "eligibility_summary": s.get("eligibility"),
            "benefits": s.get("benefits"),
            "apply_link": s.get("apply_link"),
            "score": score
        }
        for score, s in scored[:k]
    ]


# ---------------------------------------------------
# Build Prompt for Gemini (RAG + AI reasoning)
# ---------------------------------------------------
def build_prompt(user: RecommendRequest, schemes: List[Dict], top_k: int):

    scheme_text = ""
    for i, s in enumerate(schemes, start=1):
        scheme_text += f"""
Scheme {i}:
Name: {s.get("name")}
Category: {s.get("category")}
State: {s.get("state")}
Level: {s.get("level")}
Eligibility: {s.get("eligibility")}
Benefits: {s.get("benefits")}
Apply: {s.get("apply_link")}
---
"""

    return f"""
You are an expert government scheme advisor AI.

USER PROFILE:
Age: {user.age}
Gender: {user.gender}
State: {user.state}
Category: {user.category}
Occupation: {user.occupation}
Income: {user.income}
Additional text: {user.free_text}

SEMANTICALLY MATCHED SCHEMES:
{scheme_text}

TASK:
Recommend the top {top_k} schemes for the user.

Return ONLY a JSON array like:

[
  {{
    "name": "",
    "why_fit": "",
    "eligibility_summary": "",
    "benefits": "",
    "apply_link": "",
    "score": 0
  }}
]

NO explanations. NO markdown. ONLY JSON.
"""


# ---------------------------------------------------
# MAIN ENDPOINT — RAG + Gemini
# ---------------------------------------------------
@router.post("/recommend")
async def recommend(req: RecommendRequest):

    # Build query string for embedding
    query_string = " ".join([
        str(req.age or ""),
        str(req.gender or ""),
        str(req.state or ""),
        str(req.category or ""),
        str(req.occupation or ""),
        str(req.income or ""),
        str(req.free_text or "")
    ]).strip()

    if not query_string:
        raise HTTPException(status_code=400, detail="No user input provided.")

    # 1️⃣ Generate embedding
    embedding = embed_texts([query_string])[0]

    # 2️⃣ Query Vectorstore
    result = vector_query(embedding, top_k=req.top_k or 3)
    schemes = result["metadatas"][0] if result["metadatas"] else []

    if not schemes:
        raise HTTPException(status_code=500, detail="Vectorstore empty. Run seeding script.")

    # 3️⃣ Build prompt
    prompt = build_prompt(req, schemes, req.top_k or 3)

    # 4️⃣ Call Gemini
    try:
        raw = await call_gemini(prompt, max_output_tokens=700)

        # Extract JSON
        match = re.search(r"\[.*\]", raw, re.S)
        json_text = match.group(0) if match else raw

        parsed = json.loads(json_text)

        return {
            "source": "gemini",
            "recommendations": parsed,
            "retrieved_candidates": schemes
        }

    except Exception as e:
        fallback = local_fallback(schemes, req, req.top_k or 3)

        return {
            "source": "fallback",
            "error": str(e),
            "recommendations": fallback
        }
