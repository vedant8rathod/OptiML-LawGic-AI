import os
from pathlib import Path
from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware

try:
    from dotenv import load_dotenv
    # Load .env file from backend directory
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("WARNING: python-dotenv not installed. Environment variables will be loaded from system only.")

from app.routes import predict, analyze, research, entities
from app.db.database import init_db

app = FastAPI(title="LawGic AI Backend")

# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(predict.router)
app.include_router(analyze.router)
app.include_router(research.router)
app.include_router(entities.router)

# Favicon handling to prevent 404 in browsers
FAVICON_PATH = Path(__file__).parent.parent.parent / "frontend" / "public" / "favicon.ico"

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    if FAVICON_PATH.exists():
        return FileResponse(FAVICON_PATH, media_type="image/x-icon")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/")
def root():
    return {"message": "Welcome to LawGic AI Backend"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    # Create database tables on startup (idempotent)
    try:
        init_db()
    except Exception as e:
        print(f"WARNING: Database initialization failed: {e}")
        print("INFO: App will run in demo mode")
