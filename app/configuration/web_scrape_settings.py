from .configurable_settings import ConfigurableSettings

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

DEFAULT_CONTENT_SELECTORS = [
    'article.main-content',  # Class-specific article
    'main#main-content',     # ID-specific main
    'div.article-body',      # Specific div class
    'article.entry-content',  # Specific article class
    'article',              # Generic article tag
    'main',                 # Generic main tag
    '.main-content',        # General class
    '.post-content',
    '.entry-content',
    '.page-content',
    '.content',
    '[role="main"]',
    '#main',
    '.body-content',
    '.site-content',
    '.container'
]

DEFAULT_ELEMENTS_TO_REMOVE = [
    'header', 'footer', 'nav', 'script', 'style', 'iframe',
    '.header', '.footer', '.nav', '.menu',
    '#header', '#footer', '#nav', '#menu'
]


class WebScrapeSettings(ConfigurableSettings):
    """Settings for web scraping configuration"""

    def __init__(self, values: dict[str, str | None]):
        self._scraper_folder_name = values.get(
            "SCRAPER_FOLDER_NAME") or "scrape"
        self._wait_time = int(values.get("SCRAPER_WAIT_TIME") or 1)
        self._retries = int(values.get("SCRAPER_RETRIES") or 1)
        self._timeout = int(values.get("SCRAPER_TIMEOUT") or 20000)
        self._concurrent_limit = int(
            values.get("SCRAPER_CONCURRENT_LIMIT") or 2)
        self._main_content_selectors = values.get(
            "SCRAPER_CONTENT_SELECTORS") or DEFAULT_CONTENT_SELECTORS
        self._elements_to_remove = values.get(
            "SCRAPER_ELEMENTS_TO_REMOVE") or DEFAULT_ELEMENTS_TO_REMOVE
        # Parse headers from JSON string if provided, otherwise use default
        headers_str = values.get("SCRAPER_HEADERS")
        if headers_str:
            try:
                import json
                self._headers = json.loads(headers_str)
            except json.JSONDecodeError:
                self._headers = DEFAULT_HEADERS
        else:
            self._headers = DEFAULT_HEADERS

    @property
    def scraper_folder_name(self) -> str:
        return self._scraper_folder_name

    @property
    def wait_time(self) -> int:
        return self._wait_time

    @property
    def retries(self) -> int:
        return self._retries

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def concurrent_limit(self) -> int:
        return self._concurrent_limit

    @property
    def main_content_selectors(self) -> list[str]:
        return self._main_content_selectors

    @property
    def elements_to_remove(self) -> list[str]:
        return self._elements_to_remove

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @property
    def is_configured(self) -> bool:
        return self._wait_time > 0 and self._retries > 0 and self._timeout > 0
