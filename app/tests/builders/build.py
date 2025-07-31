
from app.configuration.settings import Settings
from app.configuration.web_search_settings import WebSearchSettings
from app.core.web_search import SearchResult

from .settings_builder import build_settings, build_web_search_settings
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
