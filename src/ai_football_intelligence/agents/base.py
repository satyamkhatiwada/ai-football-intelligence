from __future__ import annotations
from pydantic import BaseModel


class AgentResult(BaseModel):
    agent: str
    summary: str
    record_ids: list[str] = []
    open_questions: list[str] = []