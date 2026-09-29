from __future__ import annotations
from pydantic import BaseModel
from ai_football_intelligence.agents.research_agent import run_research_agent
from ai_football_intelligence.agents.critic_agent import review_paper_extraction
from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.memory.store import load


class OrchestratorReport(BaseModel):
    goal: str
    papers_found: int
    papers_passed_review: int
    papers_failed_review: int
    failures: list[str] = []  # human-readable "title: problem" lines
    open_questions: list[str] = []


def run_research_and_review(goal: str, max_results: int = 5) -> OrchestratorReport:
    research_result = run_research_agent(goal, max_results=max_results)

    passed = 0
    failed = 0
    failures: list[str] = []

    for paper_id in research_result.record_ids:
        paper = load(Paper, paper_id)
        review = review_paper_extraction(paper)
        if review.passed:
            passed += 1
        else:
            failed += 1
            for problem in review.problems:
                failures.append(f"{paper.title}: {problem}")

    return OrchestratorReport(
        goal=goal,
        papers_found=len(research_result.record_ids),
        papers_passed_review=passed,
        papers_failed_review=failed,
        failures=failures,
        open_questions=research_result.open_questions,
    )