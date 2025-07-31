from configuration.settings import Settings
from core.web_search import SearchEngine, SearchResult
from injector import Binder, Module, inject, singleton


class WebSearchModule(Module):
    @inject
    def configure(self, binder: Binder, settings: Settings) -> None:
        # Get the configured search engine from settings
        search_engine = settings.web_search_settings.search_engine.lower()

        # Bind the appropriate implementation based on settings
        if search_engine == "google":
            binder.bind(SearchEngine, to=GoogleSearch, scope=singleton)
        else:  # default to DuckDuckGo
            binder.bind(SearchEngine, to=DuckDuckGoSearch, scope=singleton)


class GoogleSearch(SearchEngine):
    """Google Search implementation"""

    @inject
    def __init__(self, settings: Settings):
        self._settings = settings
        self._api_key = settings.web_search_settings.api_key
        self._search_engine_url = settings.web_search_settings.search_engine_url
        self._search_limit = settings.web_search_settings.search_limit
        if not self._api_key:
            raise ValueError("Google Search API key not configured")

    async def search(self, query: str) -> list[SearchResult]:
        try:
            if not self._api_key:
                raise ValueError("Google Search API key not configured")
            # Implementation using self._api_key
            pass
        except Exception as e:
            raise


class DuckDuckGoSearch(SearchEngine):
    """DuckDuckGo Search implementation - completely free!"""

    @inject
    def __init__(self, settings: Settings):
        self._settings = settings
        self._search_engine_url = settings.web_search_settings.search_engine_url
        self._search_limit = settings.web_search_settings.search_limit
        self._search_timeout = settings.web_search_settings.search_timeout
        self._search_retries = settings.web_search_settings.search_retries

        if not self._search_engine_url:
            raise ValueError("DuckDuckGo Search URL not configured")

    async def search(self, query: str) -> list[SearchResult]:
        try:
            url = self._search_engine_url
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'no_redirect': 1
            }
            # Implementation here
            return []
        except Exception as e:
            raise
