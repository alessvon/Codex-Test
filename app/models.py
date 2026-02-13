from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class InterviewStage(str, Enum):
    INTRO = "intro"
    EXPERIENCE = "experience"
    TOOLS = "tools"
    SOFT_SKILLS = "soft_skills"
    CLOSING = "closing"
    DONE = "done"


class ExperienceItem(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    modality: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    methodologies: List[str] = Field(default_factory=list)
    team_size: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)


class SkillRating(BaseModel):
    skill: str
    level: str
    evidence: str


class SessionState(BaseModel):
    id: str
    created_at: datetime
    stage: InterviewStage = InterviewStage.INTRO
    turn: int = 0
    transcript: List[dict] = Field(default_factory=list)
    experiences: List[ExperienceItem] = Field(default_factory=list)
    extracted_skills: List[SkillRating] = Field(default_factory=list)


class CreateSessionRequest(BaseModel):
    candidate_name: str
    target_role: str = "Product Designer"
    language: str = "es"


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    reply: str
    stage: InterviewStage
    turn: int


class SessionReport(BaseModel):
    candidate_name: str
    target_role: str
    summary: str
    skills: List[SkillRating]
    experiences: List[ExperienceItem]
    recommendation: str
