import os
import httpx
from typing import Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.ai.prompts import SYSTEM_INVESTIGATION_PROMPT
from app.ai.fallback import DeterministicFallbackEngine

class LLMService:
    """Service handling LLM provider routing and fallback execution."""

    @classmethod
    async def generate_explanation(cls, evidence_data: Dict[str, Any]) -> str:
        provider = settings.LLM_PROVIDER.lower()

        if provider == "openai" and settings.OPENAI_API_KEY:
            try:
                return await cls._call_openai(evidence_data)
            except Exception as e:
                logger.warning(f"OpenAI call failed ({e}). Falling back to template explanation engine.")

        if provider == "anthropic" and settings.ANTHROPIC_API_KEY:
            try:
                return await cls._call_anthropic(evidence_data)
            except Exception as e:
                logger.warning(f"Anthropic call failed ({e}). Falling back to template explanation engine.")

        return DeterministicFallbackEngine.generate_explanation(evidence_data)

    @classmethod
    async def _call_openai(cls, evidence: Dict[str, Any]) -> str:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_INVESTIGATION_PROMPT},
                        {"role": "user", "content": f"Structured Analytical Evidence: {evidence}"}
                    ],
                    "temperature": 0.2
                },
                timeout=15.0
            )
            data = res.json()
            return data["choices"][0]["message"]["content"]

    @classmethod
    async def _call_anthropic(cls, evidence: Dict[str, Any]) -> str:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "claude-3-haiku-20240307",
                    "system": SYSTEM_INVESTIGATION_PROMPT,
                    "messages": [
                        {"role": "user", "content": f"Structured Analytical Evidence: {evidence}"}
                    ],
                    "max_tokens": 1000
                },
                timeout=15.0
            )
            data = res.json()
            return data["content"][0]["text"]
