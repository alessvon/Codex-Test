from __future__ import annotations

import re
from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    CreateSessionRequest,
    ExperienceItem,
    InterviewStage,
    MessageResponse,
    SessionReport,
    SessionState,
    SkillRating,
)

COMPANY_HINTS = [
    "globant",
    "mercadolibre",
    "rappi",
    "nubank",
    "accenture",
    "ibm",
    "freelance",
    "startup",
]
TOOLS = [
    "figma",
    "sketch",
    "adobe xd",
    "miro",
    "notion",
    "jira",
    "maze",
    "hotjar",
    "ga4",
    "figjam",
]
METHODOLOGIES = ["design thinking", "double diamond", "lean ux", "agile", "scrum", "kanban"]
TECHNIQUES = ["entrevistas", "usability testing", "card sorting", "heuristic evaluation", "journey map", "jobs to be done"]
SOFT_SKILLS = {
    "comunicación": ["comuni", "present", "storytelling", "stakeholder"],
    "colaboración": ["equipo", "cross", "multidisciplinario", "handoff"],
    "liderazgo": ["lider", "mentoria", "facilit", "coordin"],
    "pensamiento crítico": ["decisión", "trade-off", "prioriz", "hipótesis"],
}


class InterviewEngine:
    def __init__(self) -> None:
        self.sessions: dict[str, SessionState] = {}
        self.meta: dict[str, CreateSessionRequest] = {}

    def create_session(self, payload: CreateSessionRequest) -> tuple[str, MessageResponse]:
        session_id = str(uuid4())
        self.sessions[session_id] = SessionState(id=session_id, created_at=datetime.now(timezone.utc))
        self.meta[session_id] = payload
        opener = (
            f"Hola {payload.candidate_name}, gracias por participar. "
            "Para iniciar: cuéntame brevemente tu experiencia como Product Designer y tu rol actual."
        )
        return session_id, MessageResponse(reply=opener, stage=InterviewStage.INTRO, turn=0)

    def answer(self, session_id: str, message: str) -> MessageResponse:
        state = self.sessions[session_id]
        state.turn += 1
        state.transcript.append({"role": "candidate", "content": message})
        self._extract_data(state, message)

        stage_order = [
            InterviewStage.INTRO,
            InterviewStage.EXPERIENCE,
            InterviewStage.TOOLS,
            InterviewStage.SOFT_SKILLS,
            InterviewStage.CLOSING,
            InterviewStage.DONE,
        ]
        idx = stage_order.index(state.stage)
        if state.turn % 2 == 0 and state.stage != InterviewStage.DONE:
            state.stage = stage_order[min(idx + 1, len(stage_order) - 1)]

        reply = self._next_question(state)
        state.transcript.append({"role": "interviewer", "content": reply})
        return MessageResponse(reply=reply, stage=state.stage, turn=state.turn)

    def report(self, session_id: str) -> SessionReport:
        state = self.sessions[session_id]
        meta = self.meta[session_id]
        summary = (
            f"Se registraron {len(state.experiences)} experiencias y {len(state.extracted_skills)} evidencias de habilidades. "
            "La entrevista cubrió trayectoria, herramientas, metodologías, colaboración y logros medibles."
        )
        recommendation = "Avanzar a entrevista técnica" if len(state.extracted_skills) >= 4 else "Profundizar screening"
        return SessionReport(
            candidate_name=meta.candidate_name,
            target_role=meta.target_role,
            summary=summary,
            skills=state.extracted_skills,
            experiences=state.experiences,
            recommendation=recommendation,
        )

    def _next_question(self, state: SessionState) -> str:
        if state.stage == InterviewStage.INTRO:
            return "¿Cuál fue el proyecto de diseño más retador que lideraste recientemente?"
        if state.stage == InterviewStage.EXPERIENCE:
            return "Detállame una experiencia: empresa, rol, duración, modalidad, responsabilidades y logros con métricas."
        if state.stage == InterviewStage.TOOLS:
            return "¿Qué herramientas, técnicas de research y metodologías usas con más frecuencia y por qué?"
        if state.stage == InterviewStage.SOFT_SKILLS:
            return "Cuéntame cómo colaboras con PM/Engineering y cómo manejas conflictos o trade-offs de producto."
        if state.stage == InterviewStage.CLOSING:
            return "Para cerrar: ¿qué tipo de desafíos buscas en tu próximo rol como Product Designer?"
        return "Gracias. Hemos terminado; ya puedes generar el reporte de screening."

    def _extract_data(self, state: SessionState, message: str) -> None:
        lowered = message.lower()
        if any(h in lowered for h in COMPANY_HINTS) or "empresa" in lowered:
            exp = ExperienceItem()
            exp.company = self._find_company(lowered)
            exp.role = self._extract_after_keyword(message, ["rol", "role", "cargo"])
            exp.duration = self._extract_duration(message)
            exp.modality = self._extract_modality(lowered)
            exp.team_size = self._extract_team_size(message)
            exp.tools = [t for t in TOOLS if t in lowered]
            exp.methodologies = [m for m in METHODOLOGIES if m in lowered]
            exp.techniques = [t for t in TECHNIQUES if t in lowered]
            if "logro" in lowered or "aument" in lowered or "%" in message:
                exp.achievements.append(message.strip())
            if any([exp.company, exp.role, exp.duration, exp.modality, exp.tools, exp.achievements]):
                state.experiences.append(exp)

        detected_soft = []
        for skill, hints in SOFT_SKILLS.items():
            if any(h in lowered for h in hints):
                detected_soft.append(skill)
        tool_mentions = [t for t in TOOLS if t in lowered]

        evidences = []
        evidences.extend((s, "intermedio") for s in detected_soft)
        evidences.extend((f"tool:{t}", "avanzado") for t in tool_mentions)

        for skill, level in evidences:
            state.extracted_skills.append(SkillRating(skill=skill, level=level, evidence=message.strip()[:180]))

        state.extracted_skills = self._dedupe_skills(state.extracted_skills)

    @staticmethod
    def _dedupe_skills(skills: list[SkillRating]) -> list[SkillRating]:
        seen = set()
        deduped = []
        for s in skills:
            key = (s.skill, s.level)
            if key not in seen:
                deduped.append(s)
                seen.add(key)
        return deduped

    @staticmethod
    def _extract_duration(text: str) -> str | None:
        match = re.search(r"(\d+\s*(años|año|meses|mes))", text.lower())
        return match.group(1) if match else None

    @staticmethod
    def _extract_modality(lowered: str) -> str | None:
        for mode in ["remoto", "híbrido", "presencial"]:
            if mode in lowered:
                return mode
        return None

    @staticmethod
    def _extract_team_size(text: str) -> str | None:
        match = re.search(r"(\d+\s*(personas|miembros|diseñadores))", text.lower())
        return match.group(1) if match else None

    @staticmethod
    def _extract_after_keyword(text: str, keywords: list[str]) -> str | None:
        lowered = text.lower()
        for keyword in keywords:
            if keyword in lowered:
                idx = lowered.find(keyword)
                snippet = text[idx : idx + 60]
                return snippet
        return None

    @staticmethod
    def _find_company(lowered: str) -> str | None:
        for company in COMPANY_HINTS:
            if company in lowered:
                return company.title()
        return None
