# app/tests/builders/web_scrape_builder.py

from datetime import datetime
from typing import Any

from app.core.domain import ScrapePageResult


class MockResponse:
    """Mock response object for testing"""

    def __init__(self, url: str, status_code: int, content: str, headers: dict[str, Any]):
        self.url = url
        self.status_code = status_code
        self._content = content
        self.headers = headers

    async def text(self) -> str:
        return self._content


def build_mock_response(
    *,  # Force keyword arguments
    url: str = "https://example.com/test",
    status_code: int = 200,
    content: str = "<html><body><h1>Test</h1></body></html>",
    headers: dict[str, str] | None = None,
) -> MockResponse:
    """Build a mock response for testing

    Args:
        url: The URL that was requested
        status_code: HTTP status code
        content: HTML content
        headers: Response headers
    """
    return MockResponse(
        url=url,
        status_code=status_code,
        content=content,
        headers=headers or {"content-type": "text/html"}
    )


def build_scrape_result(
    *,  # Force keyword arguments
    url: str = "https://example.com/test",
    success: bool = True,
    created_at: datetime | None = None,
    title: str | None = "Test Page",
    content: str | None = "Test content",
    error_message: str | None = None
) -> ScrapePageResult:
    """Build a scrape result for testing

    Args:
        url: The URL that was scraped
        success: Whether scraping was successful
        created_at: When the scrape occurred
        title: Page title
        content: Page content
        error_message: Error if scraping failed
    """
    return ScrapePageResult(
        url=url,
        success=success,
        created_at=created_at or datetime(2024, 1, 1, 12, 0, 0),
        title=title,
        content=content,
        error_message=error_message
    )
