# Testing Strategy

The project is set up for comprehensive testing, with a clear structure that mirrors the application's layers.

- **Unit Tests**: These should be the most numerous tests. They test individual components in isolation. For example, testing a domain entity's logic should not require a database or an API.
- **Integration Tests**: These tests verify the collaboration between components, such as testing the interaction between the API layer and the database layer.
- **Test Data Builders**: The `app/tests/builders` directory indicates a preference for the **Builder Pattern** to create test data. This approach provides a clean, readable, and maintainable way to construct complex domain objects for test scenarios (e.g., `domain_builders.py`). This is the preferred method for generating test fixtures.

## Unit Testing Approach

Unit testing is the foundation of our testing strategy. We categorize our unit tests based on what they're testing, which helps us write more focused and effective tests. Each type of test has its own patterns and best practices.

### Types of Unit Tests We Write

1. **Pure Function Tests**
   These tests verify functions that take inputs and return outputs without side effects. They're the simplest to write and maintain because they don't need mocking or complex setup.

   ```python
   def test_clean_text_removes_extra_whitespace(self, web_scraper):
       """Test pure text cleaning function"""
       text = "  Hello  \n  World  \t  "
       result = web_scraper._clean_text(text)
       assert result == "Hello World"
   ```

   - Tests functions with no side effects
   - Input → Output verification
   - No mocking needed
   - Easy to understand and maintain

2. **State Change Tests**
   These tests verify that our objects correctly update their internal state. They're important for ensuring our objects maintain consistency throughout their lifecycle.

   ```python
   async def test_scrape_page_saves_result(self, web_scraper, mock_storage):
       """Test state changes during scraping"""
       url = "https://example.com"
       mock_page = AsyncMock()

       result = await web_scraper._scrape_page(url, mock_page)

       # Verify internal state changes
       assert web_scraper._successful_requests == 1
       assert url in web_scraper._successful_urls
   ```

   - Tests methods that change object state
   - Verify state before/after
   - May need mocks for dependencies
   - Focus on state changes, not implementation details

3. **Error Handling Tests**
   Error handling is crucial for robust applications. These tests ensure our code handles failures gracefully and maintains system stability.

   ```python
   async def test_scrape_page_handles_error(self, web_scraper, mock_storage):
       """Test error handling behavior"""
       url = "https://example.com"
       mock_page = AsyncMock()
       mock_page.goto.side_effect = Exception("Failed to load")

       result = await web_scraper._scrape_page(url, mock_page)

       assert not result.success
       assert "Failed to load" in result.error_message
       assert web_scraper._failed_requests == 1
   ```

   - Tests error scenarios
   - Verify error handling behavior
   - Use mocks to simulate errors
   - Ensure system stability during failures

4. **Integration Flow Tests**
   While technically still unit tests, these verify that multiple components work together correctly within a single unit. They're valuable for testing complex workflows.

   ```python
   async def test_scrape_multiple_handles_mixed_results(self, web_scraper):
       """Test complete workflow with success/failure"""
       urls = ["success.com", "error.com", "success2.com"]

       result = await web_scraper.scrape_multiple(urls)

       assert result.successful_requests == 2
       assert result.failed_requests == 1
       assert len(result.successful_urls) == 2
   ```

   - Tests complete workflows
   - Verifies components work together
   - Uses mocks for external dependencies
   - Focuses on business outcomes

## Mocking Strategy

Mocking is essential for unit testing, but it's important to mock the right things for the right reasons. Our strategy focuses on mocking external dependencies while testing real behavior.

### When We Mock

1. **External Services**
   We mock external services to avoid network calls, ensure test reliability, and control test scenarios. This includes browsers, databases, and APIs.

   ```python
   # Mock Playwright browser
   with patch('app.infrastructure.web_scrape_services.async_playwright') as mock_playwright:
       mock_page = AsyncMock()
       mock_page.title.return_value = "Test Title"
   ```

   - Browser automation (Playwright)
   - Storage systems
   - Network calls
   - Makes tests faster and more reliable

2. **Async Operations**
   Async operations require special handling in tests. We use AsyncMock to properly simulate async behavior.

   ```python
   # Mock async methods
   storage = AsyncMock(spec=Storage)
   storage.write = AsyncMock()  # Will be awaitable
   ```

   - Use AsyncMock for async methods
   - Ensure mocks can be awaited
   - Verify async calls
   - Maintain async/await patterns

3. **Dependencies via DI**
   When using dependency injection, we mock the injected dependencies to isolate the unit under test.

   ```python
   # Mock storage injected via DI
   mock_storage = AsyncMock(spec=Storage)
   scraper = WebScraperGeneric(settings=test_settings, storage=mock_storage)
   ```

   - Mock interfaces used in DI
   - Use spec to ensure interface compliance
   - Inject mocks through constructor
   - Test units in isolation

### What We Don't Mock

We avoid mocking things that should be tested directly:

1. **Pure Functions**

   ```python
   def test_clean_text(self, web_scraper):
       # No mocks needed - pure function
       result = web_scraper._clean_text("  test  ")
       assert result == "test"
   ```

2. **Internal State**
   ```python
   # Test real counters, don't mock them
   assert scraper._successful_requests == 1
   assert scraper._failed_requests == 0
   ```

## Factory Functions for Test Data

We use factory functions organized through a facade class to create test data. This approach provides a clean, maintainable way to create test objects with sensible defaults while allowing customization.

1. **Factory Functions with Default Values**
   Each factory function creates a specific type of test object, providing sensible defaults and allowing customization through keyword arguments.

   ```python
   def build_settings(**kwargs) -> Settings:
       """Build test settings with fake values"""
       settings_dict = {
           "APP_HOST": "local",
           "LOCAL_STORAGE_PATH": "/tmp/test_storage",
           "SEARCH_ENGINE": kwargs.get("search_engine", SearchProvider.DUCKDUCKGO.value),
           "SEARCH_LIMIT": str(kwargs.get("search_limit", 10)),
           "SEARCH_TIMEOUT": str(kwargs.get("search_timeout", 30)),
           # ... more defaults ...
       }

       # Create and configure Settings instance
       settings = Settings.__new__(Settings)
       settings._settings = settings_dict
       settings._web_search_settings = WebSearchSettings(settings_dict)
       # ... set other required attributes ...
       return settings
   ```

   - Provides complete objects with sensible defaults
   - Allows selective override via kwargs
   - Handles complex object initialization
   - Uses type hints for clarity

2. **Facade Class for Organization**
   The `Build` class acts as a facade, providing a single, organized entry point to all factory functions.

   ```python
   class Build:
       """Facade for all test data factory functions"""
       @staticmethod
       def settings(**kwargs) -> Settings:
           """Factory method for Settings"""
           return build_settings(**kwargs)

       @staticmethod
       def mock_response(**kwargs) -> MockResponse:
           """Factory method for mock responses"""
           return build_mock_response(**kwargs)

       @staticmethod
       def scrape_result(**kwargs) -> ScrapePageResult:
           """Factory method for scrape results"""
           return build_scrape_result(**kwargs)
   ```

   - Centralizes access to all factory functions
   - Makes test data creation discoverable
   - Provides consistent interface
   - Simplifies imports in tests

3. **Usage in Tests**
   This approach makes test data creation simple and maintainable.

   ```python
   def test_web_scraper():
       # Create test settings with custom values
       settings = Build.settings(
           scraper_concurrent_limit=2,
           scraper_timeout=1000
       )

       # Create a mock response
       response = Build.mock_response(
           url="https://example.com",
           status_code=200
       )

       # Create a scrape result
       result = Build.scrape_result(
           url="https://example.com",
           success=True
       )
   ```

   - Simple, readable test setup
   - Only specify values that matter for the test
   - Consistent pattern across all tests
   - Reduces test maintenance burden

## Test Cleanup

Proper cleanup is essential for test isolation and reliability. We handle cleanup at multiple levels to ensure tests don't interfere with each other.

1. **Fixture Level**
   Fixtures clean up their own resources after each test.

   ```python
   @pytest.fixture
   def mock_storage():
       storage = AsyncMock(spec=Storage)
       yield storage
       storage.reset_mock()  # Clean up after each test
   ```

2. **Test Level**
   Individual test cases reset object state to ensure test isolation.

   ```python
   @pytest.fixture
   def web_scraper(test_settings, mock_storage):
       scraper = WebScraperGeneric(settings=test_settings, storage=mock_storage)
       yield scraper
       # Reset state after each test
       scraper._total_requests = 0
       scraper._successful_requests = 0
   ```

3. **Global Level** (in conftest.py)
   Global cleanup handles artifacts that accumulate across test runs.

   ```python
   def pytest_sessionfinish(session, exitstatus):
       """Clean up after all tests"""
       # Clean up test artifacts
       for dirpath, dirnames, filenames in os.walk(root_dir):
           if 'MagicMock' in dirnames:
               shutil.rmtree(os.path.join(dirpath, 'MagicMock'))
   ```
