"""Render a MatchResult into a human-readable Markdown report."""

from __future__ import annotations

from .matcher import MatchResult


def format_report(result: MatchResult) -> str:
    """Build a Markdown summary: overall score, gaps first, then covered items."""
    if not result.matches:
        return "Not enough text to analyze. Paste fuller resume / job text."

    lines = [f"## Overall match: {result.overall:.0%}\n"]

    gaps = sorted(result.gaps, key=lambda m: m.score)
    if gaps:
        lines.append("### ⚠️ Gaps: requirements your resume does not clearly show")
        lines.append("*Add these if you have them, or address them before applying.*\n")
        lines += [f"- **{m.score:.0%}**: {m.requirement}" for m in gaps]
        lines.append("")

    covered = sorted(result.covered, key=lambda m: m.score, reverse=True)
    if covered:
        lines.append("### ✓ Covered requirements")
        for m in covered:
            lines.append(
                f"- **{m.score:.0%}**: {m.requirement}  \n"
                f'  <sub>matched: "{m.best_match}"</sub>'
            )

    return "\n".join(lines)
