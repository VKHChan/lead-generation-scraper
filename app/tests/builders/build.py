
from configuration import Settings
from configuration.web_search_settings import WebSearchSettings
from core.domain import ScrapePageResult, SearchResult

from .settings_builder import build_settings, build_web_search_settings
from .web_scrape_builder import MockResponse, build_mock_response, build_scrape_result
from .web_search_builder import build_default_search_result


class Build:
    """Base builder class following the Builder Pattern"""

    @staticmethod
    def search_result(**kwargs) -> SearchResult:
        """Factory method for SearchResultBuilder"""
        return build_default_search_result(**kwargs)

    @staticmethod
    def settings(**kwargs) -> Settings:
        """Factory method for Settings"""
        return build_settings(**kwargs)

    @staticmethod
    def web_search_settings(**kwargs) -> WebSearchSettings:
        """Factory method for WebSearchSettings"""
        return build_web_search_settings(**kwargs)

    @staticmethod
    def mock_response(**kwargs) -> MockResponse:
        """Factory method for mock responses"""
        return build_mock_response(**kwargs)

    @staticmethod
    def scrape_result(**kwargs) -> ScrapePageResult:
        """Factory method for scrape results"""
        return build_scrape_result(**kwargs)
