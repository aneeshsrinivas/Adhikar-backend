# app/firebase.py

import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
KEY_PATH = os.path.join(BASE_DIR, "firebase-key.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
firebase_auth = auth
