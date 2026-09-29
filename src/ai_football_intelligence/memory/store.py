from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel
from ai_football_intelligence.config import settings

def _folder_for(record: BaseModel) -> Path:
    kind = type(record).__name__.lower() + "s"  # Paper -> "papers"
    folder = Path(settings.memory_dir) / kind
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def save(record: BaseModel) -> Path:
    folder = _folder_for(record)
    path = folder / f"{record.id}.json"
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path

def load(model_cls: type[BaseModel], record_id: str) -> BaseModel:
    kind = model_cls.__name__.lower() + "s"
    path = Path(settings.memory_dir) / kind / f"{record_id}.json"
    return model_cls.model_validate_json(path.read_text(encoding="utf-8"))

def list_all(model_cls: type[BaseModel]) -> list[BaseModel]:
    kind = model_cls.__name__.lower() + "s"
    folder = Path(settings.memory_dir) / kind
    if not folder.exists():
        return []
    return [
        model_cls.model_validate_json(f.read_text(encoding="utf-8"))
        for f in sorted(folder.glob("*.json"))
    ]