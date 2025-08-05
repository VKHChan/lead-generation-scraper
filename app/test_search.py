#!/usr/bin/env python
"""
Simple script to test the search functionality using ServiceCollection.
Run this script directly to perform a search and see the results.
"""
import asyncio
import logging
import os
import sys

from app.core.web_search import SearchEngine
from app.infrastructure.service_collection import ServiceCollection

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
    # Initialize services
    service_provider = ServiceCollection.add_services()

    # Get the configured search engine from the service provider
    search_engine = service_provider.get(SearchEngine)

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
