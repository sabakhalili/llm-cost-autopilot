from app.config import settings
from app.router.providers.anthropic_provider import AnthropicProvider
from app.router.providers.base import ModelProvider
from app.router.providers.mock_provider import MockProvider
from app.router.providers.openai_provider import OpenAIProvider

_mock_provider = MockProvider()
_real_providers: dict[str, ModelProvider] = {
    "openai": OpenAIProvider(),
    "anthropic": AnthropicProvider(),
}


def get_provider(provider_name: str) -> ModelProvider:
    """Single choke point for the mock/real switch — callers just ask for a
    provider by name and never need to know whether MOCK_MODE is on."""
    if settings.mock_mode:
        return _mock_provider
    return _real_providers[provider_name]
