from fastapi.testclient import TestClient

from app.main import app


def test_screening_flow_extracts_experience_and_report():
    client = TestClient(app)

    create = client.post(
        "/api/session",
        json={"candidate_name": "Ana", "target_role": "Product Designer", "language": "es"},
    )
    assert create.status_code == 200
    session_id = create.json()["session_id"]

    msg1 = "Trabajé en Globant como Senior Product Designer por 3 años en modalidad remoto."
    r1 = client.post(f"/api/session/{session_id}/message", json={"message": msg1})
    assert r1.status_code == 200

    msg2 = "Usé Figma, Miro y Design Thinking para discovery con entrevistas y usability testing."
    r2 = client.post(f"/api/session/{session_id}/message", json={"message": msg2})
    assert r2.status_code == 200

    report = client.get(f"/api/session/{session_id}/report")
    assert report.status_code == 200
    payload = report.json()

    assert payload["candidate_name"] == "Ana"
    assert len(payload["experiences"]) >= 1
    assert any(s["skill"].startswith("tool:") for s in payload["skills"])
