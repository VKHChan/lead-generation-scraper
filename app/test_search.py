#!/usr/bin/env python
"""
Simple script to test the DuckDuckGo search functionality.
Run this script directly to perform a search and see the results.
"""
import asyncio
import logging
import os
import sys

from app.configuration.settings import get_settings
from app.infrastructure.web_search_services import DuckDuckGoSearch

# Configure logging to show all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_search():
    """Run a test search and print the results"""
    # Create Settings object using the singleton getter
    settings = get_settings()

    # Create search engine
    search_engine = DuckDuckGoSearch(settings)

    # Get search query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "python programming"
    print(f"Searching for: {query}")

    # Perform search
    results = await search_engine.search(query)

    # Print results
    if results:
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"Title: {result.title}")
            print(f"URL: {result.url}")
            print(f"Description: {result.description[:100]}...")
    else:
        print("No results found or an error occurred.")


if __name__ == "__main__":
    asyncio.run(test_search())
