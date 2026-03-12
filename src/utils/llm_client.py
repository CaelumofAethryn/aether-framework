import os
import requests


class LLMClient:
    """Simple backend-selectable LLM client."""

    def __init__(self, provider="ollama", base_url=None, api_key=None, model=None, timeout=120):
        self.provider = (provider or "ollama").lower()
        self.base_url = base_url or self._default_base_url(self.provider)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or self._default_model(self.provider)
        self.timeout = timeout

    def _default_base_url(self, provider):
        if provider == "ollama":
            return "http://127.0.0.1:11434"
        if provider in {"ooba", "oobabooga", "text-generation-webui"}:
            return "http://127.0.0.1:5000"
        if provider in {"lmstudio", "openai-compatible"}:
            return "http://127.0.0.1:1234"
        if provider == "openai":
            return "https://api.openai.com"
        return "http://127.0.0.1:11434"

    def _default_model(self, provider):
        if provider == "ollama":
            return "mistral-local:latest"
        if provider in {"lmstudio", "openai-compatible"}:
            return "local-model"
        if provider in {"ooba", "oobabooga", "text-generation-webui"}:
            return "default"
        if provider == "openai":
            return "gpt-4o-mini"
        return "mistral-local:latest"

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
