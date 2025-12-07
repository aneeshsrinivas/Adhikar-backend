# app/schemas/schemes.py
from typing import Optional
from pydantic import BaseModel

class Scheme(BaseModel):
    name: str
    level: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    eligibility: Optional[str] = None
    benefits: Optional[str] = None
    apply_link: Optional[str] = None

class SchemesResponse(BaseModel):
    count: int
    schemes: list[Scheme]
