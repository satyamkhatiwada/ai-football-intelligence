from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.orchestrator import run_research_and_review
from ai_football_intelligence.tools import research, extraction


def test_orchestrator_chains_research_and_critic(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    def fake_search(query, max_results=5):
        return [
            Paper(title="Good Paper", url="https://a.com", source="arxiv",
                  summary="Uses tracking method X on dataset Y."),
            Paper(title="Bad Paper", url="https://b.com", source="arxiv",
                  summary="Vague abstract."),
        ]
    monkeypatch.setattr(research, "search_arxiv", fake_search)

    # First call returns a good extraction, second returns a bad one
    responses = iter([
'{"method": "Deep learning tracker", "dataset": "SoccerNet tracking dataset", "limitation": "unknown"}',
        '{"method": "unknown", "dataset": "unknown", "limitation": "unknown"}',
    ])
    monkeypatch.setattr(extraction, "call_llm", lambda prompt, system=None: next(responses))

    report = run_research_and_review("test goal", max_results=2)

    assert report.papers_found == 2
    assert report.papers_passed_review == 1
    assert report.papers_failed_review == 1
    assert "Bad Paper" in report.failures[0]