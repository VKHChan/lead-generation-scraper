from datetime import datetime

from core.domain import SearchResult


def build_default_search_result(
    *,  # Force keyword arguments
    title: str = "Test Title",
    url: str = "https://example.com",
    description: str = "Test Description",
    created_at: datetime | None = None,
    source: str = "test",
    snippet: str | None = "Test Snippet"
) -> SearchResult:
    """Build default search result with optional overrides

    Args:
        title: The title of the search result
        url: The URL of the search result
        description: The description text
        date: Timestamp, defaults to current time if None
        source: Source identifier
        snippet: Optional snippet text
    """
    return SearchResult(
        title=title,
        url=url,
        description=description,
        created_at=created_at or datetime(2024, 1, 1, 12, 0, 0),
        source=source,
        snippet=snippet,
    )
