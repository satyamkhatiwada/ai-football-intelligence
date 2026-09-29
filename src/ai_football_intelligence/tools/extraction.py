from __future__ import annotations
import json
from pydantic import BaseModel, ValidationError
from ai_football_intelligence.llm import call_llm


class PaperExtraction(BaseModel):
    method: str
    dataset: str
    limitation: str


EXTRACTION_SYSTEM_PROMPT = (
    "You are a precise research assistant. Given a paper abstract, extract its "
    "method, dataset, and one limitation. Respond with ONLY valid JSON, no other "
    "text, no markdown code fences. Use exactly this shape: "
    '{"method": "...", "dataset": "...", "limitation": "..."} '
    'If a field cannot be determined from the abstract, use the string "unknown".'
)


def extract_paper_info(abstract: str) -> PaperExtraction:
    raw = call_llm(abstract, system=EXTRACTION_SYSTEM_PROMPT)
    cleaned = raw.strip()

    # Some models wrap JSON in ```json ... ``` even when told not to. Strip it defensively.
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
        return PaperExtraction(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Could not parse LLM output as valid extraction:\n{raw}") from e