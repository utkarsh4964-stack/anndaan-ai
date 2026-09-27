from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import facilities, surplus, redistribution, forecast, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Anndaan.AI",
    description="AI-powered smart food waste reduction & redistribution platform (SIH PS 26234)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facilities.router)
app.include_router(surplus.router)
app.include_router(redistribution.router)
app.include_router(forecast.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Anndaan.AI backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}
