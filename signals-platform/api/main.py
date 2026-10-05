# api/main.py
from fastapi import FastAPI
from api.routers import ecom, markets_dev, spotify # <--- Add spotify here

app = FastAPI(
    title="Signals Platform API",
    description="Unified API serving cross-domain intelligence: Markets, Developer Activity, E-Commerce, and Quantified Self.",
    version="1.0.0"
)

# Register domain routers
app.include_router(ecom.router, prefix="/api/v1")
app.include_router(markets_dev.router, prefix="/api/v1")
app.include_router(spotify.router, prefix="/api/v1") # <--- Add this line

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "signals-platform-api"}