from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from openai import OpenAI


class OpenRouterClient:
    """Thin wrapper around OpenRouter via the OpenAI Python SDK."""
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        referer: Optional[str] = None,
        site_title: Optional[str] = None,
    ) -> None:
        load_dotenv()  # read .env if present

        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("Missing API key. Set API_KEY or OPENROUTER_API_KEY in environment or .env.")

        # Use environment variables or defaults 
        self.model = model or os.getenv("OPENROUTER_MODEL") or os.getenv("MODEL") or "openai/gpt-oss-120b"
        self.base_url = base_url or os.getenv("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
        self.referer = referer or os.getenv("OPENROUTER_HTTP_REFERER") or os.getenv("HTTP_REFERER")
        self.site_title = site_title or os.getenv("OPENROUTER_SITE_TITLE") or os.getenv("SITE_TITLE")

        # OpenAI SDK v1 client configured for OpenRouter
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat_completion(self, messages: List[Dict[str, Any]]) -> str:
        """Send a list of chat messages and return assistant text."""
        headers: Dict[str, str] = {}
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.site_title:
            headers["X-Title"] = self.site_title

        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_headers=headers or None,
            extra_body={},  # placeholder for any OpenRouter-specific body fields
        )
        return (resp.choices[0].message.content or "").strip()