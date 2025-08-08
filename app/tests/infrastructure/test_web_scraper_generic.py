# app/tests/infrastructure/test_web_scraper_generic.py

from unittest.mock import AsyncMock, patch

import pytest
from core.storage import Storage
from infrastructure.web_scrape_services import WebScraperGeneric
from tests.builders.build import Build


@pytest.fixture
def mock_storage():
    storage = AsyncMock(spec=Storage)
    storage.write = AsyncMock()
    yield storage
    # Clean up mock
    storage.reset_mock()


@pytest.fixture
def test_settings():
    return Build.settings(
        scraper_concurrent_limit=2,
        scraper_wait_time=0,
        scraper_retries=1,
        scraper_timeout=1000
    )


@pytest.fixture
def web_scraper(test_settings, mock_storage):
    scraper = WebScraperGeneric(settings=test_settings, storage=mock_storage)
    yield scraper
    # Reset internal counters and lists
    scraper._total_requests = 0
    scraper._successful_requests = 0
    scraper._failed_requests = 0
    scraper._failed_urls.clear()
    scraper._successful_urls.clear()


class TestWebScraperGeneric:
    """Test each responsibility of WebScraperGeneric"""

    def test_clean_text_removes_extra_whitespace(self, web_scraper):
        """Test the text cleaning function"""
        text = "  Hello  \n  World  \t  "
        result = web_scraper._clean_text(text)
        assert result == "Hello World"

    @pytest.mark.asyncio
    async def test_extract_content_uses_selectors(self, web_scraper):
        """Test content extraction using selectors"""
        # Setup mock page
        mock_page = AsyncMock()
        mock_element = AsyncMock()
        mock_element.text_content.return_value = "Important Content"
        mock_page.query_selector.return_value = mock_element

        # Test
        content = await web_scraper._extract_content(mock_page)

        # Verify
        assert content == "Important Content"
        mock_page.query_selector.assert_called()  # Verify selector was used

    @pytest.mark.asyncio
    async def test_scrape_page_saves_result(self, web_scraper, mock_storage):
        """Test that successful scrape is saved"""
        # Setup
        url = "https://example.com"
        mock_page = AsyncMock()
        mock_page.title.return_value = "Test Title"
        mock_page.query_selector.return_value.text_content.return_value = "Test Content"

        # Test
        result = await web_scraper._scrape_page(url, mock_page)

        # Verify
        assert result.success
        assert result.title == "Test Title"
        assert result.content == "Test Content"
        mock_storage.write.assert_called_once()  # Verify result was saved

    @pytest.mark.asyncio
    async def test_scrape_page_handles_error(self, web_scraper, mock_storage):
        """Test error handling in page scraping"""
        # Setup
        url = "https://example.com"
        mock_page = AsyncMock()
        mock_page.goto.side_effect = Exception("Failed to load")

        # Test
        result = await web_scraper._scrape_page(url, mock_page)

        # Verify
        assert not result.success
        assert "Failed to load" in result.error_message
        mock_storage.write.assert_not_called()  # Verify failed result not saved

    @pytest.mark.asyncio
    async def test_scrape_multiple_handles_mixed_results(self, web_scraper):
        """Test scraping multiple URLs with mixed success/failure"""
        # Setup - URLs to test
        urls = [
            "https://example.com/success1",
            "https://example.com/error",
            "https://example.com/success2"
        ]

        # Mock playwright context
        with patch('app.infrastructure.web_scrape_services.async_playwright') as mock_playwright:
            # Setup success page
            success_page = AsyncMock()
            success_page.title.return_value = "Success Page"
            success_page.query_selector.return_value.text_content.return_value = "Success Content"
            success_page.goto = AsyncMock()  # Will succeed

            # Setup error page
            error_page = AsyncMock()
            error_page.goto.side_effect = Exception("Failed to load")

            # Setup browser context to return different pages
            mock_context = AsyncMock()
            mock_context.new_page.side_effect = [
                success_page, error_page, success_page]
            mock_context.route = AsyncMock()

            # Setup browser chain
            mock_browser = AsyncMock()
            mock_browser.new_context.return_value = mock_context
            mock_chromium = AsyncMock()
            mock_chromium.launch.return_value = mock_browser
            mock_playwright_instance = AsyncMock()
            mock_playwright_instance.chromium = mock_chromium
            mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance

            # Test
            result = await web_scraper.scrape_multiple(urls)

            # Verify results
            assert result.total_requests == 3
            assert result.successful_requests == 2
            assert result.failed_requests == 1
            assert len(result.successful_urls) == 2
            assert len(result.failed_urls) == 1
            assert "https://example.com/error" in result.failed_urls
            assert "https://example.com/success1" in result.successful_urls
            assert "https://example.com/success2" in result.successful_urls

            # Verify concurrent behavior
            assert mock_context.new_page.call_count == 3  # Created page for each URL
            assert mock_browser.close.call_count == 1  # Browser was closed
