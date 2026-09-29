from __future__ import annotations
import httpx
from ai_football_intelligence.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_llm(prompt: str, system: str | None = None) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = httpx.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {settings.groq_api_key}"},
        json={
            "model": settings.default_model,
            "messages": messages,
            "temperature": 0.2,
        },
        timeout=30.0,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Groq API error {response.status_code}: {response.text}")
    data = response.json()
    return data["choices"][0]["message"]["content"]