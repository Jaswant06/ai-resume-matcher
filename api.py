from fastapi import FastAPI
from pydantic import BaseModel

from src import analyze, format_report

app = FastAPI(title="AI Resume Matcher API")


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

@app.post("/match", response_model=MatchResponse)
def match(req: MatchRequest):
    result = analyze(req.resume, req.job)
    return MatchResponse(
        overall=result.overall,
        covered=[
            RequirementOut(requirement=m.requirement, score=m.score, best_match=m.best_match)
            for m in result.covered
        ],
        gaps=[
            RequirementOut(requirement=m.requirement, score=m.score, best_match=m.best_match)
            for m in result.gaps
        ],
    )