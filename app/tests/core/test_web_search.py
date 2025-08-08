from datetime import datetime

import pytest

from app.core.domain import SearchProvider
from app.core.web_search import SearchEngine
from app.tests.builders.build import Build


def test_search_result_creation():
    """Test creating a SearchResult with all fields"""
    result = Build.search_result()
    assert result.title == "Test Title"
    assert result.url == "https://example.com"
    assert result.description == "Test Description"
    assert result.source == "test"
    assert result.snippet == "Test Snippet"
    assert result.created_at == datetime(2024, 1, 1, 12, 0, 0)


def test_search_result_optional_fields():
    """Test SearchResult with optional fields as None"""
    result = Build.search_result(snippet=None)
    assert result.snippet is None


def test_search_provider_values():
    """Test SearchProvider enum values"""
    assert SearchProvider.GOOGLE == "google"
    assert SearchProvider.DUCKDUCKGO == "duckduckgo"


@pytest.mark.asyncio
async def test_search_engine_requires_implementation():
    """Test that SearchEngine requires implementation"""
    class TestSearchEngine(SearchEngine):
        pass  # No implementation of search method

    engine = TestSearchEngine()
    with pytest.raises(NotImplementedError):
        await engine.search("test query")
