from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.memory.store import save
from ai_football_intelligence.tools import research


def test_search_and_store_skips_existing(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    # Pre-save a paper with a specific URL
    existing = Paper(title="Already Have This", url="https://arxiv.org/abs/9999.99999",
                      source="arxiv")
    save(existing)

    # Fake arxiv search: returns one paper we already have, one we don't
    def fake_search(query, max_results=5):
        return [
            existing,
            Paper(title="Brand New Paper", url="https://arxiv.org/abs/1111.11111",
                  source="arxiv"),
        ]
    monkeypatch.setattr(research, "search_arxiv", fake_search)

    new = research.search_and_store("anything", max_results=5)

    assert len(new) == 1
    assert new[0].title == "Brand New Paper"