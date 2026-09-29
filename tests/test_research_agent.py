from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.agents import research_agent
from ai_football_intelligence.tools import research, extraction


def test_research_agent_finds_and_enriches_papers(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    # Fake arXiv: always returns one brand-new paper
    def fake_search(query, max_results=5):
        return [
            Paper(
                title="Fake Paper About Cameras",
                url="https://arxiv.org/abs/0000.00000",
                source="arxiv",
                summary="This paper does X using method Y on dataset Z.",
            )
        ]
    monkeypatch.setattr(research, "search_arxiv", fake_search)

    # Fake Groq: always returns valid extraction JSON, no real API call
    def fake_call_llm(prompt, system=None):
        return '{"method": "Method Y", "dataset": "Dataset Z", "limitation": "unknown"}'
    monkeypatch.setattr(extraction, "call_llm", fake_call_llm)

    result = research_agent.run_research_agent("cameras", max_results=1)

    assert "Fake Paper" not in result.summary  # summary shouldn't leak raw titles
    assert len(result.record_ids) == 1
    assert result.open_questions == []


def test_research_agent_reports_enrichment_failure(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    def fake_search(query, max_results=5):
        return [
            Paper(
                title="Paper With No Summary",
                url="https://arxiv.org/abs/1111.11111",
                source="arxiv",
                summary=None,  # this will make enrich_paper raise ValueError
            )
        ]
    monkeypatch.setattr(research, "search_arxiv", fake_search)

    result = research_agent.run_research_agent("cameras", max_results=1)

    assert result.record_ids == []
    assert len(result.open_questions) == 1
    assert "Paper With No Summary" in result.open_questions[0]