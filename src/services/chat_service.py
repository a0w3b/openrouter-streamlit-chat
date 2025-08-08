from __future__ import annotations

from typing import List, Dict, Any

from models.message import Message
from api.openrouter_client import OpenRouterClient


class ChatService:
    def __init__(self, client: OpenRouterClient) -> None:
        self.client = client

    def process_message(self, user_message: Message, history: List[Message] | None = None) -> Message:
        """Build message list and call OpenRouter."""
        msgs: List[Dict[str, Any]] = []
        if history:
            for m in history:
                role = "user" if m.sender.lower() == "user" else "assistant"
                msgs.append({"role": role, "content": m.content})
        msgs.append({"role": "user", "content": user_message.content})

        reply_text = self.client.chat_completion(msgs)
        return Message(content=reply_text, sender="Model")