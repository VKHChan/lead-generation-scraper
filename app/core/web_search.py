"""
Models for web search using search engine API.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SearchProvider(Enum):
    """
    Represents a search provider.
    """
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"


class SearchResult(BaseModel):
    """
    Represents a search result from a web search engine.
    """
    title: str = Field(description="The title of the search result.")
    url: str = Field(description="The URL of the search result.")
    description: str = Field(
        description="The description of the search result.")
    created_at: datetime = Field(
        description="The date and time the job was created")
    source: str = Field(description="The source of the search result.")
    snippet: str | None = Field(
        description="The snippet of the search result.")


class SearchEngine():
    """Abstract base class for search engine implementations"""

    async def search(self, query: str) -> list[SearchResult] | None:
        """Execute search and return standardized results"""
        raise NotImplementedError("Subclasses must implement this method")
