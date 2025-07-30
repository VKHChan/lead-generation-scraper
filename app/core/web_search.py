"""
Models for web search using search engine API.
"""
from datetime import datetime
from enum import Enum

from pydantic import Field
from pydantic.dataclasses import dataclass


class SearchProvider(Enum):
    """
    Represents a search provider.
    """
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"


@dataclass
class SearchResult:
    """
    Represents a search result from a web search engine.
    """
    title: str = Field(description="The title of the search result.")
    url: str = Field(description="The URL of the search result.")
    description: str = Field(
        description="The description of the search result.")
    date: datetime = Field(description="The date of the search result.")
    source: str = Field(description="The source of the search result.")
    snippet: str | None = Field(
        description="The snippet of the search result.")


class SearchEngine():
    """Abstract base class for search engine implementations"""

    async def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        """Execute search and return standardized results"""
        raise NotImplementedError("Subclasses must implement this method")
