"""API tests using FastAPI's TestClient (no running server needed)."""

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

RESUME = """Experienced Python developer building machine learning models.
Strong background in deep learning with PyTorch.
Deployed models to production as REST APIs."""

JOB = """Hiring a machine learning engineer with strong Python skills.
Experience deploying models to production is required."""


def test_health_ok():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_match_returns_structured_response():
    res = client.post("/match", json={"resume": RESUME, "job": JOB})
    assert res.status_code == 200

    body = res.json()
    assert set(body) == {"overall", "covered", "gaps"}
    assert 0.0 <= body["overall"] <= 1.0
    # every covered/gap item has the RequirementOut shape
    for item in body["covered"] + body["gaps"]:
        assert set(item) == {"requirement", "score", "best_match"}


def test_missing_field_is_rejected_by_validation():
    # no "job" key -> Pydantic rejects it before our code runs
    res = client.post("/match", json={"resume": RESUME})
    assert res.status_code == 422


def test_blank_text_returns_400():
    res = client.post("/match", json={"resume": "   ", "job": "   "})
    assert res.status_code == 400


def test_unusable_text_returns_422():
    # real strings, but too short to produce any requirement chunks
    res = client.post("/match", json={"resume": "hi", "job": "hello"})
    assert res.status_code == 422
