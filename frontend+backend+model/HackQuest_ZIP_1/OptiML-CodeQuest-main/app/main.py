from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import predict, analyze  # added analyze route
from app.db.database import init_db

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

@app.get("/")
def root():
    return {"message": "Welcome to LawGic AI Backend"}


@app.on_event("startup")
async def on_startup():
    # Initialize database, but don't crash the app if DB is unavailable locally
    try:
        await init_db()
    except Exception as e:
        print(f"⚠️ Skipping DB init (unavailable): {e}")