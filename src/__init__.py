"""AI Resume Matcher: semantic resume / job-description matching."""

from .matcher import MatchResult, RequirementMatch, analyze, chunk
from .report import format_report

__all__ = ["analyze", "chunk", "format_report", "MatchResult", "RequirementMatch"]
