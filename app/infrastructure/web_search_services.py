import asyncio
import json
import logging
import time
from datetime import datetime

from configuration.settings import Settings
from core.domain import SearchProvider
from core.storage import Storage
from core.utils import StandardFileNaming
from core.web_search import SearchEngine, SearchResult
from ddgs import DDGS
from injector import Binder, Module, inject


class WebSearchModule(Module):
    def __init__(self, search_engine: str):
        self.search_engine = search_engine

    def configure(self, binder: Binder) -> None:
        # Get the configured search engine from settings
        search_engine = self.search_engine.lower()

        # Bind the appropriate implementation based on settings
        if search_engine == SearchProvider.GOOGLE:
            binder.bind(SearchEngine, to=GoogleSearch)
        elif search_engine == SearchProvider.DUCKDUCKGO:
            binder.bind(SearchEngine, to=DuckDuckGoSearch)
        else:
            raise ValueError(
                f"Invalid search engine: {search_engine}. Must be one of: {SearchProvider.GOOGLE}, {SearchProvider.DUCKDUCKGO}")


class GoogleSearch(SearchEngine):
    """Google Search implementation"""

    @inject
    def __init__(self, settings: Settings, storage: Storage):
        self._settings = settings
        self._api_key = settings.web_search_settings.api_key
        self._search_engine_url = settings.web_search_settings.search_engine_url
        self._search_limit = settings.web_search_settings.search_limit
        self._file_naming = StandardFileNaming()
        if not self._api_key:
            raise ValueError("Google Search API key not configured")

    async def search(self, query: str) -> list[SearchResult] | None:
        try:
            if not self._api_key:
                raise ValueError("Google Search API key not configured")
            # Implementation using self._api_key
            return None
        except Exception as e:
            raise


class DuckDuckGoSearch(SearchEngine):
    """DuckDuckGo Search implementation using duckduckgo-search library"""

    @inject
    def __init__(self, settings: Settings, storage: Storage):
        self._settings = settings
        self._search_limit = settings.web_search_settings.search_limit
        self._search_timeout = settings.web_search_settings.search_timeout
        self._search_retries = settings.web_search_settings.search_retries
        self._storage = storage
        self._file_naming = StandardFileNaming()

        # Create the DDGS client
        self._ddgs = DDGS(timeout=self._search_timeout)

    async def search(self, query: str) -> list[SearchResult] | None:
        """Search DuckDuckGo for the given query"""
        try:
            logging.info(f"Starting DuckDuckGo search for query: {query}")

            # Run the search in an executor to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self._search_with_retries(query)
            )

            if not results:
                logging.info("No results found")
                return None

            # Convert to SearchResult objects
            search_results = []
            count = 0
            for result in results:
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('href', ''),
                    description=result.get('body', ''),
                    created_at=datetime.now(),
                    source='DuckDuckGo',
                    snippet=result.get('body', '')
                )
                count += 1
                if count > self._search_limit:
                    break
                search_results.append(search_result)

                # Store each result in storage as json in the dated folder
                # Create folder hierarchy YYYY/MM/DD
                now = datetime.now()
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")

                folder_name = f"{self._settings.web_search_settings.search_folder_name}/{year}/{month}/{day}"
                file_name = f"{folder_name}/{self._file_naming.clean_url_for_file(result.get('href', ''))}_search.json"
                self._storage.write(
                    file_name,
                    search_result.model_dump()
                )

            logging.info(
                f"Search successful, found {len(search_results)} results")
            return search_results

        except Exception as e:
            logging.error(f"Error in DuckDuckGo search: {str(e)}")
            return None

    def _search_with_retries(self, query: str) -> list[dict]:
        """Execute search with retries"""
        retry_count = 0
        max_retries = self._search_retries
        all_results = []

        while retry_count <= max_retries:
            try:
                # Use the text search method from duckduckgo_search
                results = list(self._ddgs.text(
                    query,
                    region='wt-wt',  # Worldwide results
                    safesearch='moderate',
                    timelimit=None,  # No time limit
                    # Get more than we need in case some are filtered
                    max_results=self._search_limit * 2
                ))

                # Filter out ads and sponsored results
                filtered_results = [
                    result for result in results
                    if not self._is_ad_or_sponsored(result.get('href', ''))
                ]

                logging.debug(f"Raw search results: {filtered_results}")
                return filtered_results

            except Exception as e:
                retry_count += 1
                if retry_count > max_retries:
                    logging.error(
                        f"DuckDuckGo search failed after {max_retries} retries: {str(e)}")
                    return all_results

                logging.warning(
                    f"Search attempt {retry_count} failed: {str(e)}. Retrying...")
                time.sleep(2 ** retry_count)  # Exponential backoff

        return all_results

    def _is_ad_or_sponsored(self, url: str) -> bool:
        """Check if a URL is likely an ad or sponsored result"""
        if not url:
            return False

        # Common ad URL patterns
        ad_patterns = [
            'aclick?',
            '/aclk?',
            'adurl=',
            '/ads/',
            'doubleclick',
            'googleadservices',
            'pagead'
        ]

        return any(pattern in url.lower() for pattern in ad_patterns)
