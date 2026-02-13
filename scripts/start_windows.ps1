$ErrorActionPreference = "Stop"

if (-Not (Test-Path ".venv/Scripts/python.exe")) {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    py -m venv .venv
  }
  elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python -m venv .venv
  }
  else {
    throw "No se encontró Python. Instala Python 3.11+ y marca 'Add Python to PATH'."
  }
}

.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
