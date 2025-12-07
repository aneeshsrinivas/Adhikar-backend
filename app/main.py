from dotenv import load_dotenv
load_dotenv()

# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# Routers
from app.routes.schemes import router as schemes_router
from app.routes.recommend import router as recommend_router
from app.routes.auth import router as auth_router
from app.routes.user_actions import router as user_actions_router
from app.routes.applications import router as applications_router   # <-- NEW


# ---------------------------------
# Create FastAPI App
# ---------------------------------
app = FastAPI(
    title="JanSevak AI - Backend",
    version="1.0.0",
    description="Backend API for JanSevak AI (Govt Scheme Recommender + OTP Auth + Application Tracking)"
)


# ---------------------------------
# Custom Swagger With Bearer Auth
# ---------------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add Authorize button
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply bearer auth to all endpoints automatically
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ---------------------------------
# Register Routers
# ---------------------------------

# Public scheme listing & search
app.include_router(schemes_router, prefix="/api", tags=["Schemes"])

# AI Recommendation (vector + Gemini)
app.include_router(recommend_router, prefix="/api", tags=["AI Recommendation"])

# OTP Login + Email Auth
app.include_router(auth_router, tags=["Auth"])

# User actions → saved schemes, history, feedback
app.include_router(user_actions_router, tags=["User Actions"])

# Scheme Application Tracking (NEW)
app.include_router(applications_router, prefix="/api", tags=["Applications"])


# ---------------------------------
# Home Route
# ---------------------------------
@app.get("/")
def home():
    return {"message": "Adhikar Backend Running 🚀"}
