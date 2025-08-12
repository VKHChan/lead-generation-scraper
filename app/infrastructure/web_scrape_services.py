import asyncio
import json
import logging
from datetime import datetime

from configuration import Settings
from core.domain import ScrapePageResult
from core.storage import Storage
from core.utils import StandardFileNaming
from core.web_scrape import ScrapingResult, WebScraper
from injector import Binder, Module, inject
from playwright.async_api import Page, async_playwright

DEFAULT_SUCCESS_STATUS = "success"
DEFAULT_FAILED_STATUS = "failed"

logger = logging.getLogger(__name__)


class WebScraperModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(WebScraper, to=WebScraperGeneric)


class WebScraperGeneric(WebScraper):
    @inject
    def __init__(self, storage: Storage, settings: Settings):
        self._storage = storage
        self._scrape_settings = settings.web_scrape_settings
        logger.info(f"Scrape settings: {self._scrape_settings}")
        self._file_naming = StandardFileNaming()

        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._failed_urls = []
        self._successful_urls = []

    async def scrape_multiple(self, urls: list[str], file_path: str = None) -> ScrapingResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                java_script_enabled=False,
                viewport={'width': 1280, 'height': 720},
                user_agent=self._scrape_settings.headers['User-Agent']
            )
            # Define a route interception to block images, media, fonts, and JavaScript files

            async def route_intercept(route, request):
                if request.resource_type in ["image", "media", "font", "script"]:
                    await route.abort()
                else:
                    await route.continue_()

            # Apply route interception at the context level so it affects all pages
            await context.route("**/*", route_intercept)

            sem = asyncio.Semaphore(self._scrape_settings.concurrent_limit)

            async def process_url(url):
                async with sem:
                    page = None
                    try:
                        page = await context.new_page()
                        result = await self._scrape_page(url, page, file_path)

                        return result
                    finally:
                        if page:
                            await page.close()

            try:
                tasks = [asyncio.create_task(process_url(url)) for url in urls]
                await asyncio.gather(*tasks)
            finally:
                await browser.close()
        return self._get_statistics()

    async def _scrape_page(self, url: str, page: Page, file_path: str = None) -> ScrapePageResult:
        self._total_requests += 1
        for attempt in range(self._scrape_settings.retries):
            try:
                # Handle popups
                page.on("dialog", lambda dialog: asyncio.create_task(
                    dialog.dismiss()))
                page.on("popup", lambda popup: asyncio.create_task(popup.close()))

                await page.goto(url,
                                timeout=self._scrape_settings.timeout,
                                wait_until='networkidle')
                logger.info(f"Page loaded: {url}")
                logger.info(f"Page title: {await page.title()}")
                content = await self._extract_content(page)
                result = ScrapePageResult(
                    url=url,
                    created_at=datetime.now(),
                    title=await page.title(),
                    content=content,
                    success=True,
                    error_message=None
                )

                self._successful_requests += 1
                self._successful_urls.append(url)

                status = DEFAULT_SUCCESS_STATUS if result.success else DEFAULT_FAILED_STATUS
                folder_name = f"{self._scrape_settings.scraper_folder_name}/{status}"
                if file_path:
                    folder_name = f"{file_path}/{self._scrape_settings.scraper_folder_name}/{status}"

                file_name = f"{folder_name}/{self._file_naming.clean_url_for_file(url)}_scraped.json"
                await asyncio.to_thread(
                    self._storage.write_json,
                    file_name,
                    result.model_dump()
                )

                return result
            except Exception as e:
                if attempt < self._scrape_settings.retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    self._failed_requests += 1
                    self._failed_urls.append(url)
                    return ScrapePageResult(
                        url=url,
                        created_at=datetime.now(),
                        title=None,
                        content=None,
                        success=False,
                        error_message=str(e)
                    )

    async def _extract_content(self, page: Page) -> str:
        """Efficient content extraction that stops at first valid selector"""
        for selector in self._scrape_settings.main_content_selectors:
            selector = selector.strip()
            if not selector:
                continue

            logger.debug(f"Trying selector: {selector}")

            try:
                # Find first matching element
                element = await page.query_selector(selector)

                if element:
                    # Get text content immediately
                    text = await element.text_content()
                    cleaned_text = self._clean_text(text)

                    # Check if content is meaningful
                    if cleaned_text and len(cleaned_text) > 50:
                        logger.info(f"Selected content from {selector}")
                        return cleaned_text

            except Exception as e:
                logger.debug(f"Error with selector {selector}: {str(e)}")
                continue

        # Fallback to body if no content found
        try:
            body = await page.query_selector('body')
            if body:
                content = await body.text_content()
                cleaned_content = self._clean_text(content)
                return cleaned_content
        except Exception as e:
            logger.error(f"Fallback content extraction failed: {str(e)}")

        # Absolute fallback
        return ''

    def _clean_text(self, text: str) -> str:
        """Clean extracted text by removing excessive whitespace"""
        if not text:
            return ""
        # Replace tabs and newlines with spaces
        text = text.replace('\t', ' ').replace('\n', ' ')
        # Remove multiple spaces
        text = ' '.join(text.split())
        return text.strip()

    def _get_statistics(self) -> ScrapingResult:
        """Get scraping statistics"""
        return ScrapingResult(
            total_requests=self._total_requests,
            successful_requests=self._successful_requests,
            failed_requests=self._failed_requests,
            failed_urls=self._failed_urls,
            successful_urls=self._successful_urls
        )
