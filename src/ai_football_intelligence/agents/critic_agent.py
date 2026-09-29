from __future__ import annotations
from ai_football_intelligence.records.models import Paper, ReviewResult
from ai_football_intelligence.memory.store import save


MIN_FIELD_LENGTH = 10


def review_paper_extraction(paper: Paper) -> ReviewResult:
    problems: list[str] = []

    if paper.method is None or paper.dataset is None:
        problems.append("Extraction was never run on this paper (method/dataset missing)")
    else:
        if paper.method == "unknown" and paper.dataset == "unknown":
            problems.append("Both method and dataset came back 'unknown' — extraction may have failed silently")
        if paper.method != "unknown" and len(paper.method) < MIN_FIELD_LENGTH:
            problems.append(f"Method description suspiciously short: '{paper.method}'")
        if paper.dataset != "unknown" and len(paper.dataset) < MIN_FIELD_LENGTH:
            problems.append(f"Dataset description suspiciously short: '{paper.dataset}'")

    result = ReviewResult(
        paper_id=paper.id,
        passed=len(problems) == 0,
        problems=problems,
    )
    save(result)
    return result