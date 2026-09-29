from __future__ import annotations
from ai_football_intelligence.agents.base import AgentResult
from ai_football_intelligence.tools.research import search_and_store
from ai_football_intelligence.tools.extraction import enrich_paper


def run_research_agent(goal: str, max_results: int = 5) -> AgentResult:
    """
    Given a research goal (used directly as a search query for now),
    find new papers, save them, and enrich each with extracted info.
    """
    new_papers = search_and_store(goal, max_results=max_results)

    enriched_ids = []
    open_questions = []

    for paper in new_papers:
        try:
            enrich_paper(paper)
            enriched_ids.append(paper.id)
        except Exception as e:
            # Don't let one bad paper kill the whole batch.
            open_questions.append(f"Could not enrich '{paper.title}': {e}")

    summary = (
        f"Found {len(new_papers)} new paper(s) for '{goal}'. "
        f"Successfully enriched {len(enriched_ids)}."
    )

    return AgentResult(
        agent="research",
        summary=summary,
        record_ids=enriched_ids,
        open_questions=open_questions,
    )