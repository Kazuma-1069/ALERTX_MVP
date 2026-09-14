from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.database import init_db
    from backend.api.contacts import router as contacts_router
    from backend.api.emergency import router as emergency_router
except ImportError:
    from database import init_db
    from api.contacts import router as contacts_router
    from api.emergency import router as emergency_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AlertX Emergency Backend",
    version="0.1.0",
    description="Minimal FastAPI backend for AlertX MVP emergency response system",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(emergency_router, prefix="/emergency", tags=["emergency"])


@app.get("/health")
def health_check():
    return {"status": "ok"}