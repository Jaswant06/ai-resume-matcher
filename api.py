"""FastAPI REST API for the resume matcher.

A thin HTTP layer over `src.analyze`. The matching logic lives in `src/`;
this file only handles requests, validation, and JSON responses.

Run locally:
    uvicorn api:app --reload      # docs at http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src import analyze
from src.matcher import get_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the embedding model once, at startup, before any request.

    Without this the model would load lazily on the first /match call, so the
    first user would wait several seconds. Warming it here moves that cost to
    startup, where it belongs.
    """
    get_model()
    yield


app = FastAPI(title="AI Resume Matcher API", version="1.0.0", lifespan=lifespan)


class MatchRequest(BaseModel):
    resume: str
    job: str


class RequirementOut(BaseModel):
    requirement: str
    score: float
    best_match: str


class MatchResponse(BaseModel):
    overall: float
    covered: list[RequirementOut]
    gaps: list[RequirementOut]


def _to_out(matches) -> list[RequirementOut]:
    """Convert the engine's RequirementMatch dataclasses into response models."""
    return [
        RequirementOut(requirement=m.requirement, score=m.score, best_match=m.best_match)
        for m in matches
    ]


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check. Used by Docker / load balancers to know the app is up."""
    return {"status": "ok"}


@app.post("/match", response_model=MatchResponse)
def match(req: MatchRequest) -> MatchResponse:
    if not req.resume.strip() or not req.job.strip():
        raise HTTPException(
            status_code=400,
            detail="Both 'resume' and 'job' must contain text.",
        )

    result = analyze(req.resume, req.job)

    if not result.matches:
        raise HTTPException(
            status_code=422,
            detail="Not enough usable text to analyze. Provide fuller resume and job text.",
        )

    return MatchResponse(
        overall=result.overall,
        covered=_to_out(result.covered),
        gaps=_to_out(result.gaps),
    )
