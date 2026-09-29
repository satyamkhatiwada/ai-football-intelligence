from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.agents.critic_agent import review_paper_extraction


def test_flags_paper_never_enriched(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    paper = Paper(title="Unenriched Paper", url="https://a.com", source="arxiv")
    result = review_paper_extraction(paper)

    assert result.passed is False
    assert "never run" in result.problems[0]


def test_flags_double_unknown(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    paper = Paper(title="Vague Paper", url="https://b.com", source="arxiv",
                  method="unknown", dataset="unknown", limitation="unknown")
    result = review_paper_extraction(paper)

    assert result.passed is False
    assert any("unknown" in p for p in result.problems)


def test_passes_good_extraction(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    paper = Paper(title="Good Paper", url="https://c.com", source="arxiv",
                  method="Uses a deep learning tracker with Kalman filtering",
                  dataset="SoccerNet tracking dataset", limitation="unknown")
    result = review_paper_extraction(paper)

    assert result.passed is True
    assert result.problems == []