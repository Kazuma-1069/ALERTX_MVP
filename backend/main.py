from fastapi import FastAPI
from backend.api.contacts import router as contacts_router
from backend.api.emergency import router as emergency_router

app = FastAPI(title="ALERTX MVP", version="0.1.0")

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(emergency_router, prefix="/emergency", tags=["emergency"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "ALERTX"}
