"""LLM API wrapper for OpenAI and Anthropic models."""
import os
import time
from typing import Optional, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from config import (
    API_TEMPERATURE, API_MAX_TOKENS, API_TIMEOUT,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY
)


class LLMClient:
    """Unified client for OpenAI and Anthropic APIs."""

    def __init__(self, provider: str, model_id: str):
        self.provider = provider
        self.model_id = model_id

        if provider == "openai":
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        elif provider == "anthropic":
            self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        elif provider == "openrouter":
            self.client = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = API_TEMPERATURE,
        max_tokens: int = API_MAX_TOKENS,
        max_retries: int = 3,
        retry_delay: float = 2.0
    ) -> str:
        """Generate a completion for the given prompt."""
        for attempt in range(max_retries):
            try:
                if self.provider in ["openai", "openrouter"]:
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": prompt})

                    response = self.client.chat.completions.create(
                        model=self.model_id,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=API_TIMEOUT
                    )
                    return response.choices[0].message.content.strip()

                elif self.provider == "anthropic":
                    response = self.client.messages.create(
                        model=self.model_id,
                        max_tokens=max_tokens,
                        system=system_prompt if system_prompt else "",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.content[0].text.strip()

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"API error (attempt {attempt + 1}): {e}")
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise e

        return ""


def create_client(model_name: str, models_config: Dict) -> LLMClient:
    """Create an LLM client from model configuration."""
    if model_name not in models_config:
        raise ValueError(f"Unknown model: {model_name}")

    config = models_config[model_name]
    return LLMClient(config["provider"], config["model_id"])


if __name__ == "__main__":
    # Test API connections
    from config import MODELS

    for model_name, config in MODELS.items():
        print(f"\nTesting {model_name}...")
        try:
            client = create_client(model_name, MODELS)
            response = client.complete(
                "What is 2 + 2? Reply with just the number.",
                system_prompt="You are a helpful assistant."
            )
            print(f"  Response: {response}")
        except Exception as e:
            print(f"  Error: {e}")
