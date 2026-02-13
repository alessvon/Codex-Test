#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
python -m uvicorn app.main:app --reload --port 8000
