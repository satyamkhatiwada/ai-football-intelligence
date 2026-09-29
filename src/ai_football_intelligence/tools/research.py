from __future__ import annotations
from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.memory.store import save, list_all
from ai_football_intelligence.tools.arxiv import search_arxiv


def search_and_store(query: str, max_results: int = 5) -> list[Paper]:
    """Search arXiv, save any papers not already in memory, return only the new ones."""
    existing_urls = {p.url for p in list_all(Paper)}

    results = search_arxiv(query, max_results=max_results)
    new_papers = [p for p in results if p.url not in existing_urls]

    for paper in new_papers:
        save(paper)

    return new_papers