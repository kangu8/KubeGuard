
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.responses import FileResponse

from app.models import SecurityEvent, SecurityEventCreate
from app.database import init_db, save_event, get_events as load_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="KubeGuard Security API",
    description="Security Events API for the KubeGuard DevSecOps Platform",
    version="0.3.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "application": "KubeGuard Security API",
        "version": "0.3.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/ready")
def readiness():
    return {"status": "ready"}


@app.post(
    "/events",
    response_model=SecurityEvent,
    status_code=status.HTTP_201_CREATED
)
def create_event(event: SecurityEventCreate):
    new_event = SecurityEvent(
        **event.model_dump(),
        id=str(uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat()
    )

    save_event(new_event)
    return new_event


@app.get("/events", response_model=list[SecurityEvent])
def list_events():
    return load_events()


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    dashboard_path = (
        Path(__file__).resolve().parent
        / "static"
        / "dashboard.html"
    )
    return FileResponse(dashboard_path)
