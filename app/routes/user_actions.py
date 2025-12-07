# app/routes/user_actions.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from app.firebase import db
from app.routes.auth import verify_token

router = APIRouter(prefix="/api/user", tags=["User Actions"])


# ------------------------------------------------
# MODELS
# ------------------------------------------------
class SaveSchemePayload(BaseModel):
    scheme_id: str
    note: Optional[str] = None


class HistoryPayload(BaseModel):
    query: Dict
    recommendations: List[Dict]


# ------------------------------------------------
# SAVE SCHEME (BOOKMARK)
# ------------------------------------------------
@router.post("/save-scheme")
def save_scheme(payload: SaveSchemePayload, user=Depends(verify_token)):
    uid = user.get("uid")

    if not uid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    entry = {
        "scheme_id": payload.scheme_id,
        "note": payload.note,
        "saved_at": datetime.utcnow().isoformat(),
    }

    db.collection("users").document(uid).collection("saved_schemes").add(entry)

    return {"status": "success", "message": "Scheme saved", "saved": entry}


# ------------------------------------------------
# LIST SAVED SCHEMES
# ------------------------------------------------
@router.get("/saved-schemes")
def list_saved(user=Depends(verify_token)):
    uid = user.get("uid")

    docs = db.collection("users").document(uid).collection("saved_schemes").stream()
    items = [d.to_dict() for d in docs]

    return {"count": len(items), "saved": items}


# ------------------------------------------------
# SAVE RECOMMENDATION HISTORY
# ------------------------------------------------
@router.post("/history")
def save_history(payload: HistoryPayload, user=Depends(verify_token)):
    uid = user.get("uid")

    entry = {
        "query": payload.query,
        "recommendations": payload.recommendations,
        "timestamp": datetime.utcnow().isoformat(),
    }

    db.collection("users").document(uid).collection("history").add(entry)

    return {"status": "success", "message": "History saved", "entry": entry}


# ------------------------------------------------
# GET HISTORY (LATEST FIRST)
# ------------------------------------------------
@router.get("/history")
def get_history(user=Depends(verify_token)):
    uid = user.get("uid")

    docs = (
        db.collection("users")
        .document(uid)
        .collection("history")
        .order_by("timestamp")
        .stream()
    )

    history = [d.to_dict() for d in docs]

    return {"count": len(history), "history": history}
