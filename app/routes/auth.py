# app/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.firebase import firebase_auth, db
import os
import requests
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])

# ------------------------------------------------
# MODELS
# ------------------------------------------------

class SignupPayload(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    language_pref: Optional[str] = None


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class SendOtpPayload(BaseModel):
    phone_number: str


class VerifyOtpPayload(BaseModel):
    sessionInfo: str
    otp: str


class UpdateProfilePayload(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    language_pref: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


# ------------------------------------------------
# VERIFY TOKEN (Used by /me and update-profile)
# ------------------------------------------------

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    id_token = authorization.split(" ", 1)[1]

    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


# ------------------------------------------------
# 1) SEND OTP (BACKEND)
# ------------------------------------------------

@router.post("/send-otp")
def send_otp(payload: SendOtpPayload):

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing FIREBASE_WEB_API_KEY")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendVerificationCode?key={api_key}"

    resp = requests.post(url, json={"phoneNumber": payload.phone_number})
    data = resp.json()

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=data)

    return {"sessionInfo": data["sessionInfo"]}


# ------------------------------------------------
# 2) VERIFY OTP → LOGIN
# ------------------------------------------------

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpPayload):

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPhoneNumber?key={api_key}"

    body = {"sessionInfo": payload.sessionInfo, "code": payload.otp}

    resp = requests.post(url, json=body)
    data = resp.json()

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=data)

    idToken = data["idToken"]
    refreshToken = data["refreshToken"]
    uid = data["localId"]
    phone = data.get("phoneNumber")

    # Save profile if new user
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        db.collection("users").document(uid).set({
            "uid": uid,
            "phone_number": phone,
            "email": None,
            "state": None,
            "district": None,
            "occupation": None,
            "language_pref": None,
            "created_at": datetime.utcnow().isoformat()
        })

    return {
        "status": "success",
        "idToken": idToken,
        "refreshToken": refreshToken,
        "uid": uid,
        "phone": phone
    }


# ------------------------------------------------
# EMAIL SIGNUP (OPTIONAL)
# ------------------------------------------------

@router.post("/signup")
def signup(payload: SignupPayload):

    if not payload.email or not payload.password:
        raise HTTPException(
            status_code=400,
            detail="Email signup requires email + password"
        )

    try:
        user_record = firebase_auth.create_user(
            email=payload.email,
            password=payload.password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    uid = user_record.uid

    profile = {
        "uid": uid,
        "email": payload.email,
        "phone_number": payload.phone_number,
        "state": payload.state,
        "district": payload.district,
        "occupation": payload.occupation,
        "language_pref": payload.language_pref,
        "created_at": datetime.utcnow().isoformat()
    }

    db.collection("users").document(uid).set(profile)

    return {"uid": uid, "message": "Signup successful"}


# ------------------------------------------------
# EMAIL LOGIN
# ------------------------------------------------

@router.post("/login")
def login(payload: LoginPayload):

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    resp = requests.post(url, json={
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    })

    data = resp.json()

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=data)

    return {
        "idToken": data["idToken"],
        "refreshToken": data["refreshToken"],
        "expiresIn": data["expiresIn"],
        "uid": data["localId"]
    }


# ------------------------------------------------
# PROFILE DETAILS
# ------------------------------------------------

@router.get("/me")
def get_profile(user=Depends(verify_token)):

    uid = user["uid"]
    doc = db.collection("users").document(uid).get()

    # FIXED BUG → "exists" is property
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User profile not found")

    return doc.to_dict()


# ------------------------------------------------
# UPDATE PROFILE
# ------------------------------------------------

@router.put("/update-profile")
def update_profile(payload: UpdateProfilePayload, user=Depends(verify_token)):

    uid = user["uid"]

    updates = {k: v for k, v in payload.dict().items() if v is not None}

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Update Firestore
    db.collection("users").document(uid).set(updates, merge=True)

    # Return updated profile
    new_doc = db.collection("users").document(uid).get()

    return {"message": "Profile updated", "profile": new_doc.to_dict()}


# ------------------------------------------------
# REFRESH TOKEN
# ------------------------------------------------

@router.post("/refresh")
def refresh_token(refresh_token: str):

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    resp = requests.post(url, data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    data = resp.json()

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=data)

    return data


# ------------------------------------------------
# LOGOUT (REVOKE TOKENS)
# ------------------------------------------------

@router.post("/revoke")
def revoke_tokens(user=Depends(verify_token)):

    uid = user["uid"]

    try:
        firebase_auth.revoke_refresh_tokens(uid)
        return {"status": "success", "message": "User tokens revoked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
