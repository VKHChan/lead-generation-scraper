from core.domain import SearchResult


class SearchEngine:
    """Abstract base class for search engine implementations"""

    async def search(self, query: str) -> list[SearchResult] | None:
        """Execute search and return standardized results"""
        raise NotImplementedError("Subclasses must implement this method")
