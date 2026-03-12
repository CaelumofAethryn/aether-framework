import requests

from src.config.aether_config import (
    get_api_key,
    get_base_url,
    get_model,
    get_provider,
    get_timeout,
)

class LLMClient:
    """Simple backend-selectable LLM client."""

    def __init__(self, provider=None, base_url=None, api_key=None, model=None, timeout=None):
        self.provider = (provider or get_provider()).lower()
        self.base_url = base_url or get_base_url(self.provider)
        self.api_key = api_key or get_api_key()
        self.model = model or get_model(self.provider)
        self.timeout = timeout if timeout is not None else get_timeout()


    def generate_text(self, prompt, model=None, temperature=0.7, max_tokens=512):
        return self.send_request(
            prompt=prompt,
            model=model or self.model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def send_request(self, prompt, model=None, temperature=0.7, max_tokens=512):
        model = model or self.model

        if self.provider == "ollama":
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature},
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", str(data))

        raise ValueError(f"Unsupported provider: {self.provider}")
