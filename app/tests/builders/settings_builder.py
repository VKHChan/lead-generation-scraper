from faker import Faker

from app.configuration.settings import Settings
from app.configuration.web_search_settings import WebSearchSettings
from app.core.web_search import SearchProvider


def build_web_search_settings(
    *,
    search_engine: SearchProvider | None = None,
    api_key: str | None = None,
    search_limit: str | None = None,
    search_timeout: str | None = None,
    search_retries: str | None = None,
        search_engine_url: str | None = None) -> WebSearchSettings:
    fake = Faker()
    values = {
        "SEARCH_ENGINE": search_engine or fake.random_element(elements=[p.value for p in SearchProvider]),
        "API_KEY": api_key or fake.uuid4(),
        "SEARCH_LIMIT": search_limit or str(fake.random_int(min=1, max=10)),
        "SEARCH_TIMEOUT": search_timeout or str(fake.random_int(min=1, max=10)),
        "SEARCH_RETRIES": search_retries or str(fake.random_int(min=1, max=5)),
        "SEARCH_ENGINE_URL": search_engine_url or fake.url()
    }
    return WebSearchSettings(values)


def build_settings(**kwargs) -> Settings:
    """Build test settings with fake values"""
    # Create a Settings instance without calling __init__
    settings = Settings.__new__(Settings)
    Settings._instance = settings

    # Create web search settings
    web_search_settings = build_web_search_settings(**kwargs)

    # Set attributes directly
    settings._web_search_settings = web_search_settings

    return settings
