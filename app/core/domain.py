from dataclasses import asdict, fields
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


class SearchProvider:
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


class ModelHost:
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    AWS = "aws"


class ModelProvider:
    ANTHROPIC = "anthropic"


class ScrapePageResult(BaseModel):
    url: str = Field(description="The URL to scrape")
    success: bool = Field(description="Whether the scraping was successful")
    created_at: datetime = Field(
        description="The date and time the job was created")
    title: str | None = Field(description="The title of the scraped page")
    content: str | None = Field(description="The content of the scraped page")
    error_message: str | None = Field(
        description="The error message if the scraping failed")


class ScrapingResult(BaseModel):
    total_requests: int = Field(
        description="The total number of requests made")
    successful_requests: int = Field(
        description="The number of successful requests")
    failed_requests: int = Field(
        description="The number of failed requests")
    failed_urls: list[str] = Field(
        description="The URLs that failed to be scraped")
    successful_urls: list[str] = Field(
        description="The URLs that were successfully scraped")


@dataclass
class BaseSettings:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> list[str]:
        return [f.name for f in fields(cls)]


@dataclass(frozen=True)
class ChatModelSettings:
    host: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    streaming: bool = True
    force_tool_support: bool = False
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int | None = None
