from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, Field


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


class ClaimStatus(str, Enum):
    UNVERIFIED = "unverified"
    SUPPORTED = "supported"
    REJECTED = "rejected"


class Paper(BaseModel):
    id: str = Field(default_factory=lambda: new_id("paper"))
    title: str
    authors: list[str] = []
    year: int | None = None
    url: str
    source: str  # e.g. "arxiv", "openalex"
    summary: str | None = None
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Evidence(BaseModel):
    id: str = Field(default_factory=lambda: new_id("evid"))
    description: str
    source_url: str
    paper_id: str | None = None


class Claim(BaseModel):
    id: str = Field(default_factory=lambda: new_id("claim"))
    statement: str
    status: ClaimStatus = ClaimStatus.UNVERIFIED
    evidence_ids: list[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_note: str | None = None