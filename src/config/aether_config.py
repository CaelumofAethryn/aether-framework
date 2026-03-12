import os


DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OOBA_BASE_URL = "http://127.0.0.1:5000"
DEFAULT_LMSTUDIO_BASE_URL = "http://127.0.0.1:1234"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com"

DEFAULT_OLLAMA_MODEL = "mistral-local:latest"
DEFAULT_LMSTUDIO_MODEL = "local-model"
DEFAULT_OOBA_MODEL = "default"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

DEFAULT_TIMEOUT = 120


def get_provider():
    provider = os.getenv("AETHER_LLM_PROVIDER", DEFAULT_PROVIDER)
    return provider.lower()


def get_base_url(provider=None):
    provider = (provider or get_provider()).lower()

    env_base_url = os.getenv("AETHER_LLM_BASE_URL")
    if env_base_url:
        return env_base_url

    if provider == "ollama":
        return DEFAULT_OLLAMA_BASE_URL
    if provider in {"ooba", "oobabooga", "text-generation-webui"}:
        return DEFAULT_OOBA_BASE_URL
    if provider in {"lmstudio", "openai-compatible"}:
        return DEFAULT_LMSTUDIO_BASE_URL
    if provider == "openai":
        return DEFAULT_OPENAI_BASE_URL

    return DEFAULT_OLLAMA_BASE_URL


def get_model(provider=None):
    provider = (provider or get_provider()).lower()

    env_model = os.getenv("AETHER_LLM_MODEL")
    if env_model:
        return env_model

    if provider == "ollama":
        return DEFAULT_OLLAMA_MODEL
    if provider in {"ooba", "oobabooga", "text-generation-webui"}:
        return DEFAULT_OOBA_MODEL
    if provider in {"lmstudio", "openai-compatible"}:
        return DEFAULT_LMSTUDIO_MODEL
    if provider == "openai":
        return DEFAULT_OPENAI_MODEL

    return DEFAULT_OLLAMA_MODEL


def get_timeout():
    env_timeout = os.getenv("AETHER_LLM_TIMEOUT")
    if env_timeout:
        try:
            return int(env_timeout)
        except ValueError:
            pass
    return DEFAULT_TIMEOUT


def get_api_key():
    return os.getenv("OPENAI_API_KEY")
