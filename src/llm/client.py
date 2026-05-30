import logging
from openai import OpenAI

from src.config import (
    NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_LLM_MODEL,
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL,
    LLM_TEMPERATURE, LLM_MAX_TOKENS,
    NVIDIA_AVAILABLE, OPENROUTER_AVAILABLE,
)
from src.llm.prompts import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.nvidia_client = None
        self.openrouter_client = None

        if NVIDIA_AVAILABLE:
            self.nvidia_client = OpenAI(
                api_key=NVIDIA_API_KEY,
                base_url=NVIDIA_BASE_URL,
            )

        if OPENROUTER_AVAILABLE:
            self.openrouter_client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url=OPENROUTER_BASE_URL,
            )

        if not self.nvidia_client and not self.openrouter_client:
            raise RuntimeError(
                "Nenhum LLM configurado. Defina NVIDIA_API_KEY ou OPENROUTER_API_KEY no .env"
            )

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
    ) -> dict:
        """
        Generate a response. Tries NVIDIA NIM first, falls back to OpenRouter.
        Returns dict with 'content' and 'model_used'.
        """
        if system_prompt is None:
            system_prompt = SYSTEM_PROMPT
        if temperature is None:
            temperature = LLM_TEMPERATURE
        if max_tokens is None:
            max_tokens = LLM_MAX_TOKENS

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # Try NVIDIA first
        if self.nvidia_client:
            try:
                logger.info("Tentando NVIDIA NIM (%s)...", NVIDIA_LLM_MODEL)
                response = self.nvidia_client.chat.completions.create(
                    model=NVIDIA_LLM_MODEL,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=0.9,
                )
                content = response.choices[0].message.content
                return {"content": content, "model_used": f"nvidia:{NVIDIA_LLM_MODEL}"}
            except Exception as e:
                logger.warning("NVIDIA NIM falhou: %s", e)

        # Fallback to OpenRouter
        if self.openrouter_client:
            try:
                logger.info("Fallback para OpenRouter (%s)...", OPENROUTER_MODEL)
                response = self.openrouter_client.chat.completions.create(
                    model=OPENROUTER_MODEL,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                content = response.choices[0].message.content
                return {"content": content, "model_used": f"openrouter:{OPENROUTER_MODEL}"}
            except Exception as e:
                logger.error("OpenRouter falhou: %s", e)
                raise RuntimeError(f"Todos os provedores LLM falharam: {e}")

        raise RuntimeError("Nenhum provedor LLM disponivel")
