# app/seed_firestore.py

import json
import os
from app.firebase import db

def seed_schemes():
    # Path to seed_schemes.json inside the data folder
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed_schemes.json")

    # Load JSON data
    with open(data_path, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    # Reference to Firestore collection
    coll = db.collection("schemes")

    # Insert each scheme
    for scheme in schemes:
        doc_id = scheme["name"].replace(" ", "_").lower()
        coll.document(doc_id).set(scheme)

    print(f"Inserted {len(schemes)} schemes into Firestore successfully!")

if __name__ == "__main__":
    seed_schemes()
