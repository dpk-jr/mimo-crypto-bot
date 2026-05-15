"""
Xiaomi MiMo API Client
OpenAI-compatible interface for MiMo V2.5
"""

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class MiMoClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("MIMO_API_KEY"),
            base_url=os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1"),
        )
        self.model = os.getenv("MIMO_MODEL", "MiMo-V2.5")

    async def chat(
        self,
        message: str,
        system: str = None,
        history: list = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Send a chat completion request to MiMo API.

        Args:
            message: User message
            system: System prompt (optional)
            history: Conversation history (optional)
            temperature: Sampling temperature
            max_tokens: Max response tokens

        Returns:
            Assistant response text
        """
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": message})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ MiMo API Error: {str(e)}"

    async def chat_sync(
        self,
        message: str,
        system: str = None,
    ) -> str:
        """Simplified single-turn chat."""
        return await self.chat(message, system=system)
