"""Core matching engine.

Compares a resume against a job description using sentence embeddings. Each
requirement in the job description is matched against the most similar line in
the resume; the similarity of that best match is the requirement's coverage
score. Requirements are extracted from the job text itself; nothing is
hard-coded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from statistics import mean

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.30
MIN_WORDS = 3  # ignore fragments shorter than this when chunking

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def chunk(text: str) -> list[str]:
    """Split raw resume/job text into meaningful lines or sentences.

    Breaks on newlines, bullets and sentence terminators, then drops short
    fragments (headers, labels) that carry no requirement.
    """
    # Unglue headers that lost their line break on paste, e.g.
    # "SummaryResults" -> "Summary" / "Results", "EducationBachelor" -> split.
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", "\n", text)
    # Split on newlines, bullets, and sentence terminators that are FOLLOWED by
    # whitespace. Requiring whitespace keeps "B.Com." and "Monday.com" intact.
    parts = re.split(r"\n+|[•·]+|(?<=[.;:])\s+", text)
    cleaned = (p.strip(" \t\r\n\"',.;:") for p in parts)  # trim whitespace + edge punctuation
    return [p for p in cleaned if len(p.split()) >= MIN_WORDS]


@dataclass
class RequirementMatch:
    """How well a single job requirement is covered by the resume."""

    requirement: str
    score: float
    best_match: str
    covered: bool


@dataclass
class MatchResult:
    """The full comparison of a resume against a job description."""

    overall: float
    matches: list[RequirementMatch]

    @property
    def covered(self) -> list[RequirementMatch]:
        return [m for m in self.matches if m.covered]

    @property
    def gaps(self) -> list[RequirementMatch]:
        return [m for m in self.matches if not m.covered]


def analyze(
    resume_text: str,
    job_text: str,
    threshold: float = DEFAULT_THRESHOLD,
) -> MatchResult:
    """Match a resume against a job description and score every requirement."""
    resume_chunks = chunk(resume_text)
    job_reqs = chunk(job_text)

    if not resume_chunks or not job_reqs:
        return MatchResult(overall=0.0, matches=[])

    model = get_model()
    resume_vecs = model.encode(resume_chunks)
    req_vecs = model.encode(job_reqs)

    # Each requirement vs every resume chunk; keep each requirement's best match.
    similarities = model.similarity(req_vecs, resume_vecs)
    best = similarities.max(dim=1)

    matches = []
    for i, requirement in enumerate(job_reqs):
        score = best.values[i].item()
        matches.append(
            RequirementMatch(
                requirement=requirement,
                score=score,
                best_match=resume_chunks[int(best.indices[i])],
                covered=score >= threshold,
            )
        )

    return MatchResult(overall=mean(m.score for m in matches), matches=matches)
