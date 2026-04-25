"""LLM abstraction layer — supports OpenAI, Claude, and local models."""

import logging
from abc import ABC, abstractmethod
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        ...


class OpenAIProvider(LLMProvider):
    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        except ImportError:
            raise RuntimeError("openai package not installed")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=4000,
        )
        return response.choices[0].message.content


class ClaudeProvider(LLMProvider):
    def __init__(self):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
            self.model = settings.CLAUDE_MODEL
        except ImportError:
            raise RuntimeError("anthropic package not installed")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text


class LocalLLMProvider(LLMProvider):
    def __init__(self):
        import requests
        self.url = settings.LOCAL_LLM_URL
        if not self.url:
            raise RuntimeError("LOCAL_LLM_URL not configured")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        import requests

        payload = {
            "prompt": prompt,
            "system_prompt": system_prompt or "",
            "max_tokens": 4000,
            "temperature": 0.3,
        }
        response = requests.post(f"{self.url}/generate", json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("text", "")


class FallbackProvider(LLMProvider):
    """Fallback when no LLM is configured — generates template-based text."""

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        logger.warning("LLM not configured. Using fallback text generation.")
        return (
            "Texto gerado automaticamente pelo sistema. "
            "Para textos mais elaborados, configure um provedor LLM "
            "(OpenAI, Claude ou modelo local)."
        )


def get_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider()
    elif provider == "claude" and settings.CLAUDE_API_KEY:
        return ClaudeProvider()
    elif provider == "local" and settings.LOCAL_LLM_URL:
        return LocalLLMProvider()
    else:
        logger.info("No LLM provider configured, using fallback.")
        return FallbackProvider()
