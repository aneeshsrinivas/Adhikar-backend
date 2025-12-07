from fastapi import APIRouter, Depends, HTTPException, Header
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.firebase import db
from app.routes.auth import verify_token


router = APIRouter(prefix="/applications", tags=["Applications"])


# -------------------------------
# MODELS
# -------------------------------
class StartApplicationPayload(BaseModel):
    scheme_id: str
    scheme_name: str
    apply_link: Optional[str] = None


class UpdateStatusPayload(BaseModel):
    application_id: str
    status: str  # draft, submitted, in_review, approved, rejected


# -------------------------------
# START APPLICATION
# -------------------------------
@router.post("/start")
def start_application(payload: StartApplicationPayload, user=Depends(verify_token)):
    uid = user["uid"]

    app_ref = db.collection("user_applications").document(f"{uid}_{payload.scheme_id}")

    # If already exists, return existing record
    if app_ref.get().exists:
        return {"message": "Application already exists", "id": app_ref.id}

    data = {
        "id": app_ref.id,
        "uid": uid,
        "scheme_id": payload.scheme_id,
        "scheme_name": payload.scheme_name,
        "apply_link": payload.apply_link,
        "status": "draft",
        "stage": 1,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    app_ref.set(data)

    return {"status": "success", "application": data}


# -------------------------------
# UPDATE STATUS
# -------------------------------
@router.post("/update")
def update_status(payload: UpdateStatusPayload, user=Depends(verify_token)):
    uid = user["uid"]
    app_ref = db.collection("user_applications").document(payload.application_id)
    doc = app_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Application not found")

    current = doc.to_dict()
    if current["uid"] != uid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Map status to stage number
    status_to_stage = {
        "draft": 1,
        "submitted": 2,
        "in_review": 3,
        "approved": 4,
        "rejected": 5
    }

    updated_data = {
        "status": payload.status,
        "stage": status_to_stage.get(payload.status, 1),
        "updated_at": datetime.utcnow().isoformat()
    }

    app_ref.update(updated_data)

    return {"status": "success", "updated": updated_data}


# -------------------------------
# GET ALL APPLICATIONS FOR USER
# -------------------------------
@router.get("/my")
def my_applications(user=Depends(verify_token)):
    uid = user["uid"]
    docs = db.collection("user_applications").where("uid", "==", uid).stream()

    applications = [d.to_dict() for d in docs]

    return {"count": len(applications), "applications": applications}


# -------------------------------
# GET SINGLE APPLICATION
# -------------------------------
@router.get("/{app_id}")
def get_application(app_id: str, user=Depends(verify_token)):
    app_ref = db.collection("user_applications").document(app_id)
    doc = app_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Application not found")

    data = doc.to_dict()
    if data["uid"] != user["uid"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return data
