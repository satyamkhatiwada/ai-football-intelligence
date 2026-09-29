from __future__ import annotations
import httpx
import xml.etree.ElementTree as ET
from ai_football_intelligence.records.models import Paper

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"


def search_arxiv(query: str, max_results: int = 5) -> list[Paper]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    response = httpx.get(ARXIV_API_URL, params=params, timeout=15.0)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers: list[Paper] = []

    for entry in root.findall(f"{ATOM_NS}entry"):
        title = entry.findtext(f"{ATOM_NS}title", default="").strip()
        summary = entry.findtext(f"{ATOM_NS}summary", default="").strip()
        url = entry.findtext(f"{ATOM_NS}id", default="").strip()
        published = entry.findtext(f"{ATOM_NS}published", default="")
        year = int(published[:4]) if published else None

        authors = [
            author.findtext(f"{ATOM_NS}name", default="").strip()
            for author in entry.findall(f"{ATOM_NS}author")
        ]

        papers.append(
            Paper(
                title=title,
                authors=authors,
                year=year,
                url=url,
                source="arxiv",
                summary=summary,
            )
        )

    return papers