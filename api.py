from fastapi import FastAPI
from pydantic import BaseModel

from src import analyze, format_report

app = FastAPI(title="AI Resume Matcher API")


class MatchRequest(BaseModel):
    resume: str
    job: str


@app.post("/match")
def match(req: MatchRequest):
    result = analyze(req.resume, req.job)
    return format_report(result)