from .configurable_settings import ConfigurableSettings


class WebSearchSettings(ConfigurableSettings):
    """
    Settings for the web search.
    """

    def __init__(self, values: dict[str, str | None]):
        self._search_folder_name = values.get(
            "SEARCH_FOLDER_NAME") or "search"
        self._search_engine = values.get("SEARCH_ENGINE") or "duckduckgo"
        self._search_engine_url = values.get(
            "SEARCH_ENGINE_URL") or "https://api.duckduckgo.com/"
        self._api_key = values.get("API_KEY") or None
        self._search_limit = int(values.get("SEARCH_LIMIT") or 10)
        self._search_timeout = int(values.get("SEARCH_TIMEOUT") or 30)
        self._search_retries = int(values.get("SEARCH_RETRIES") or 3)

    @property
    def search_folder_name(self) -> str:
        return self._search_folder_name

    @property
    def search_engine(self) -> str:
        return self._search_engine

    @property
    def search_engine_url(self) -> str | None:
        return self._search_engine_url

    @property
    def api_key(self) -> str | None:
        return self._api_key

    @property
    def search_limit(self) -> int:
        return self._search_limit

    @property
    def search_timeout(self) -> int:
        return self._search_timeout

    @property
    def search_retries(self) -> int:
        return self._search_retries

    @property
    def is_configured(self) -> bool:
        return self._search_engine is not None and self._search_engine_url is not None
