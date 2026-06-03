from __future__ import annotations

import httpx

from app.config import get_settings


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def provider_name(self) -> str:
        if not self.settings.llm_api_key or self.settings.llm_provider.lower() == "mock":
            return "mock"
        return self.settings.llm_provider

    def generate(self, prompt: str, fallback: str) -> str:
        if self.provider_name == "mock":
            return fallback

        try:
            with httpx.Client(timeout=20) as client:
                response = client.post(
                    f"{self.settings.llm_base_url.rstrip('/')}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.llm_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.settings.llm_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You draft concise synthetic ambulance claim appeal letters.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.2,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return fallback
