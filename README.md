# Product Designer Screening Agent (Agentic UI MVP)

Aplicación MVP para entrevistas de **screening técnico + soft skills** para **Product Designer**.

## Qué hace
- Entrevista conversacional por etapas.
- Extrae información profesional de respuestas:
  - empresa, rol, duración, modalidad
  - responsabilidades, herramientas, técnicas y metodologías
  - tamaño de equipo y logros
- Genera un reporte de screening con habilidades detectadas y recomendación.

## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

Abrir: `http://localhost:8000`

## API principal
- `POST /api/session`
- `POST /api/session/{session_id}/message`
- `GET /api/session/{session_id}/report`

## Notas
- Este MVP usa extracción heurística local (sin LLM externo).
- Está listo para conectar un proveedor LLM en la clase `InterviewEngine`.
