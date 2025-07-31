
from app.core.web_search import SearchResult

from .web_search_builder import build_default_search_result


class Build:
    """Base builder class following the Builder Pattern"""

    @staticmethod
    def search_result(**kwargs) -> SearchResult:
        """Factory method for SearchResultBuilder"""
        return build_default_search_result(**kwargs)
