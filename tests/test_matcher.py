"""Unit tests for the matching engine."""

from src.matcher import analyze, chunk

RESUME = """Experienced Python developer building machine learning models.
Strong background in deep learning with PyTorch.
Deployed models to production as REST APIs."""

RELEVANT_JOB = """Hiring a machine learning engineer with strong Python skills.
Experience deploying models to production is required."""

UNRELATED_JOB = """Seeking a senior accountant for tax preparation.
Must be experienced in financial auditing and reporting."""


def test_chunk_drops_short_fragments():
    text = "Requirements:\nStrong Python programming skills are required."
    chunks = chunk(text)
    assert "Strong Python programming skills are required" in chunks
    assert "Requirements" not in chunks  # too short, dropped


def test_relevant_job_scores_higher_than_unrelated():
    relevant = analyze(RESUME, RELEVANT_JOB).overall
    unrelated = analyze(RESUME, UNRELATED_JOB).overall
    assert relevant > unrelated


def test_missing_skill_is_flagged_as_gap():
    job = "Must have experience with Kubernetes and Docker containers."
    result = analyze(RESUME, job)
    gap_requirements = " ".join(g.requirement.lower() for g in result.gaps)
    assert "kubernetes" in gap_requirements or "docker" in gap_requirements


def test_empty_input_returns_no_matches():
    result = analyze("", "")
    assert result.matches == []
    assert result.overall == 0.0
