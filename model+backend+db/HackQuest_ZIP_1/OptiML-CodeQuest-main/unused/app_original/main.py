from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, analyze  # added analyze route
from app.routes import research
from app.db.database import init_db
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
import app.utils.model_loader as model_loader

app = FastAPI(title="LawGic AI Backend")

# Enable CORS so frontend can communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router)
app.include_router(analyze.router)  # include the analyze route
app.include_router(research.router)  # include the research route

@app.get("/")
def root():
    return {"message": "Welcome to LawGic AI Backend"}

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok and bool(model_loader.model) else "degraded",
        "db": db_ok,
        "model_loaded": bool(model_loader.model),
    }


@app.on_event("startup")
async def on_startup():
    # Initialize database; in Docker this must succeed (db health-gated)
    await init_db()