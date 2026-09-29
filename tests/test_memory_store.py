from ai_football_intelligence.records.models import Paper
from ai_football_intelligence.memory.store import save, load, list_all


def test_save_and_load_paper(tmp_path, monkeypatch):
    # tmp_path is a pytest-provided temporary folder, deleted after the test.
    # We point memory_dir at it so tests never touch your real memory_store/.
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    paper = Paper(title="Unit Test Paper", url="https://example.com", source="manual")
    save(paper)

    loaded = load(Paper, paper.id)
    assert loaded.title == "Unit Test Paper"
    assert loaded.id == paper.id


def test_list_all_returns_saved_papers(tmp_path, monkeypatch):
    from ai_football_intelligence.config import settings
    monkeypatch.setattr(settings, "memory_dir", str(tmp_path))

    save(Paper(title="Paper A", url="https://a.com", source="manual"))
    save(Paper(title="Paper B", url="https://b.com", source="manual"))

    titles = {p.title for p in list_all(Paper)}
    assert titles == {"Paper A", "Paper B"}