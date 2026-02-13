# Product Designer Screening Agent (Agentic UI MVP)

Aplicación MVP para entrevistas de **screening técnico + soft skills** para **Product Designer**.

## Qué hace
- Entrevista conversacional por etapas.
- Extrae información profesional de respuestas:
  - empresa, rol, duración, modalidad
  - responsabilidades, herramientas, técnicas y metodologías
  - tamaño de equipo y logros
- Genera un reporte de screening con habilidades detectadas y recomendación.

## Ejecutar (Linux / macOS)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m uvicorn app.main:app --reload --port 8000
```

## Ejecutar (Windows CMD)
```bat
cd C:\ruta\a\Codex-Test
scripts\start_windows.cmd
```

## Ejecutar (Windows PowerShell)
```powershell
cd C:\ruta\a\Codex-Test
.\scripts\start_windows.ps1
```

Estos scripts:
- crean el venv si no existe,
- instalan dependencias,
- levantan la app con el Python del venv (`.venv\Scripts\python.exe`).

Abrir: `http://localhost:8000`

## Verificación rápida por API (opcional)
Con el servidor corriendo, puedes probar en otra terminal:

```bash
curl -X POST http://127.0.0.1:8000/api/session \
  -H "content-type: application/json" \
  -d '{"candidate_name":"Ana","target_role":"Product Designer","language":"es"}'
```

Si responde con `session_id`, la app está funcionando.

## Scripts rápidos
- Windows CMD: `scripts\start_windows.cmd`
- PowerShell: `scripts\start_windows.ps1`
- Linux/macOS: `bash scripts/start_unix.sh`

## API principal
- `POST /api/session`
- `POST /api/session/{session_id}/message`
- `GET /api/session/{session_id}/report`

## Troubleshooting en Windows
- Error **"source no se reconoce"**: estás en CMD/PowerShell; usa los scripts de `scripts\`.
- Error **"uvicorn no se reconoce"**: no ejecutes `uvicorn` directo; usa `python -m uvicorn` o los scripts.
- Error **"py no se reconoce"**: instala Python desde python.org o usa `python` si ya está en PATH.
- Si PowerShell bloquea scripts: ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Notas
- Este MVP usa extracción heurística local (sin LLM externo).
- Está listo para conectar un proveedor LLM en la clase `InterviewEngine`.
