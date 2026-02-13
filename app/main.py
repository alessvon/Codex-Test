from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .interview_engine import InterviewEngine
from .models import CreateSessionRequest, MessageRequest

app = FastAPI(title="Product Designer Screening Agent")
engine = InterviewEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(static_path / "index.html")


@app.post("/api/session")
def create_session(payload: CreateSessionRequest):
    session_id, first_message = engine.create_session(payload)
    return {"session_id": session_id, "message": first_message}


@app.post("/api/session/{session_id}/message")
def send_message(session_id: str, payload: MessageRequest):
    if session_id not in engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return engine.answer(session_id, payload.message)


@app.get("/api/session/{session_id}/report")
def get_report(session_id: str):
    if session_id not in engine.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return engine.report(session_id)
