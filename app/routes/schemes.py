# app/routes/schemes.py
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.firebase import db   # your firestore client
from app.schemas.schemes import Scheme, SchemesResponse

router = APIRouter(prefix="/api", tags=["Schemes"])

@router.get("/schemes", response_model=SchemesResponse)
def list_schemes(
    state: Optional[str] = Query(None, description="State name to filter"),
    category: Optional[str] = Query(None, description="Category to filter"),
    level: Optional[str] = Query(None, description="central/state/local"),
    q: Optional[str] = Query(None, description="Full-text search in name/benefits/eligibility"),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None, regex="^(name|level)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
):
    """
    List schemes with optional filters, search, pagination and sorting.
    Uses Firestore 'schemes' collection seeded in seed_firestore.py.
    """
    try:
        col_ref = db.collection("schemes")
        # Build Firestore query progressively for equality filters
        query = col_ref
        if state:
            # store states as exact value or null; Firestore supports equality
            query = query.where("state", "==", state)
        if category:
            query = query.where("category", "==", category)
        if level:
            query = query.where("level", "==", level)

        # Firestore doesn't support offset efficiently for large offsets.
        # We'll fetch (offset + limit) documents and slice client-side.
        docs = query.stream()
        items = []
        for d in docs:
            data = d.to_dict()
            # Normalize (optional) - ensure keys exist
            items.append({
                "name": data.get("name"),
                "level": data.get("level"),
                "state": data.get("state"),
                "category": data.get("category"),
                "eligibility": data.get("eligibility"),
                "benefits": data.get("benefits"),
                "apply_link": data.get("apply_link"),
            })

        # Apply q (simple case-insensitive substring search) client-side
        if q:
            q_low = q.strip().lower()
            def match(item):
                for field in ("name", "benefits", "eligibility", "category"):
                    val = item.get(field) or ""
                    if q_low in val.lower():
                        return True
                return False
            items = list(filter(match, items))

        # Sorting
        if sort_by:
            reverse = (order == "desc")
            items.sort(key=lambda x: (x.get(sort_by) or "").lower(), reverse=reverse)

        total = len(items)
        sliced = items[offset: offset + limit]

        # Convert to pydantic-compatible objects
        return {"count": total, "schemes": sliced}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing schemes: {e}")
