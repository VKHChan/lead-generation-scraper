# User Stories

## Epic 1: Pain Point Discovery

### Story 1.1: Data Collection System ✅

**As a** researcher  
**I want** to automatically collect data from various online sources about non-profit operations  
**So that** we can identify potential automation opportunities and pain points

**Implemented Features:**

1. Domain Layer ✅

   - Defined SearchResult model for structured search data
   - Defined ScrapePageResult model for scraped content
   - Created interfaces for search (SearchEngine) and scraping (WebScraper) strategies
   - Implemented standardized file naming and data organization

2. Infrastructure Layer ✅

   - Implemented DuckDuckGo search integration with configurable settings
   - Created web scraping service with error handling and retry logic
   - Built configurable rate limiting and timeout system
   - Implemented hierarchical storage system (local/S3 compatible)
   - Added data serialization with proper JSON formatting

3. Command Line Interface ✅

   - Created simple CLI for search and scrape operations
   - Implemented configurable search parameters
   - Added progress logging and result display
   - Stored results in organized directory structure (YYYY/MM/DD)

4. Testing & Configuration ✅
   - Added integration tests for search workflow
   - Implemented configurable settings via .env files
   - Added logging for debugging and monitoring
   - Created sample configuration files

### Story 1.2: LLM-Based Content Analysis

**As a** business analyst  
**I want** to use LLM to analyze each scraped article and extract structured insights  
**So that** we can build a database of pain points, solutions, and market opportunities

**Development Tasks:**

1. Domain Layer:

   - Define content analysis model:

     ```python
     class ContentAnalysis:
         """Analysis results for a single article"""
         url: str
         title: str
         analysis_date: datetime

         pain_points: list[PainPoint]
         solutions: list[Solution]
         service_providers: list[ServiceProvider]

         class PainPoint:
             description: str
             category: str
             impact: str
             source_quote: str  # Original text snippet
             context: str       # Surrounding context

         class Solution:
             name: str
             description: str
             target_pain_points: list[str]  # References to pain point descriptions
             features: list[str]
             benefits: list[str]
             pricing_info: str | None

         class ServiceProvider:
             name: str
             website: str | None
             described_solutions: list[str]  # References to solution names
             value_proposition: str
     ```

2. Infrastructure Layer:

   - Implement LLM analysis pipeline:
     - Content extraction service (clean HTML/text)
     - LLM prompt engineering for entity extraction
     - JSON response parsing and validation
   - Create storage structure:
     ```
     storage/
       └── YYYY/MM/DD/
           └── content/
               └── {url_hash}/
                   ├── raw.json        # Original scraped content
                   └── analysis.json   # LLM analysis results
     ```

3. LLM Integration:

   - Design extraction prompt:

     ```
     "Analyze this article and extract insights in JSON format:
     {
       'pain_points': [
         {
           'description': 'Clear statement of the problem',
           'category': 'Categorize the type of pain point',
           'impact': 'Describe the impact on operations',
           'source_quote': 'Exact quote from text',
           'context': 'Surrounding context of the quote'
         }
       ],
       'solutions': [...],
       'service_providers': [...]
     }

     Focus on:
     1. Specific pain points with clear impact
     2. Concrete solutions, not vague suggestions
     3. Actual service providers mentioned

     Use exact quotes where possible."
     ```

   - Implement validation:
     - JSON schema validation
     - Required fields checking
     - Quote verification
   - Add error handling:
     - LLM response parsing
     - Malformed content handling
     - Rate limiting management

4. Analysis Scripts:

   - Create aggregation tools:
     ```python
     async def aggregate_analyses(start_date: date, end_date: date):
         """Aggregate analyses across date range"""
         return {
             'pain_points': defaultdict(list),  # category -> pain points
             'solutions': defaultdict(list),     # provider -> solutions
             'providers': defaultdict(list)      # category -> providers
         }
     ```
   - Build search tools:
     ```python
     async def search_analyses(query: str,
                             content_type: Literal['pain_points', 'solutions', 'providers']):
         """Search through analyses by content type and query"""
     ```

5. Testing:
   - Single article analysis tests
   - LLM extraction accuracy tests
   - Storage integrity tests
   - Aggregation correctness tests

### Story 1.3: Job Posting Analysis System

**As a** researcher  
**I want** to analyze job postings for automation opportunities  
**So that** we can identify common operational pain points

**Development Tasks:**

1. Domain Layer:

   - Define JobPosting model
   - Create text analysis interfaces
   - Define role-pain point mapping rules

2. Infrastructure Layer:

   - Implement text analysis service
   - Create role mapping service
   - Build pattern recognition system

3. API Layer:

   - Add job posting analysis endpoints
   - Create pattern reporting endpoints
   - Implement trend analysis endpoints

4. Testing:
   - Text analysis accuracy tests
   - Pattern recognition tests
   - Role mapping validation

## Epic 2: Organization Matching

### Story 2.1: Organization Data Collection System

**As a** researcher  
**I want** to automatically collect data about Canadian non-profit organizations from various directories and networks  
**So that** we can build a comprehensive database of potential organizations

**Development Tasks:**

1. Domain Layer:

   - Define DirectorySource model for different directories (CRA, Imagine Canada, etc.)
   - Define OrganizationRawData and CollectionJob models
   - Create interfaces for directory-specific collection strategies

2. Infrastructure Layer:

   - Implement directory scraping services with rate limiting
   - Create LinkedIn organization data collector
   - Build event directory integration system
   - Implement organization data storage system
   - Create data deduplication and merging service

3. API Layer:

   - Create collection job management endpoints
   - Add directory configuration endpoints
   - Implement collection status monitoring
   - Create raw organization data access endpoints

4. Testing:
   - Directory scraper reliability tests
   - Data deduplication accuracy tests
   - Collection completeness validation
   - Integration tests with various sources

### Story 2.2: Organization Profiling System

**As a** lead researcher  
**I want** to create detailed technology context profiles for organizations  
**So that** we can understand their automation potential

**Development Tasks:**

1. Domain Layer:

   - Define Organization and TechContext models
   - Create profiling interfaces
   - Define technology assessment rules

2. Infrastructure Layer:

   - Implement profile storage system
   - Create tech stack analysis service
   - Build context tracking system

3. API Layer:

   - Create profile management endpoints
   - Add tech context endpoints
   - Implement assessment endpoints

4. Testing:
   - Profile validation tests
   - Tech context analysis tests
   - Assessment accuracy tests

### Story 2.3: Pain Point Matching Engine

**As a** business analyst  
**I want** to match organizations with relevant pain points  
**So that** we can identify high-value automation opportunities

**Development Tasks:**

1. Domain Layer:

   - Define matching rules and scoring models
   - Create priority calculation interfaces
   - Define confidence scoring rules

2. Infrastructure Layer:

   - Implement matching algorithm
   - Create scoring engine
   - Build recommendation system

3. API Layer:

   - Add matching endpoints
   - Create scoring endpoints
   - Implement recommendation endpoints

4. Testing:
   - Matching accuracy tests
   - Scoring validation tests
   - Recommendation quality tests

## Epic 3: Outreach Management

### Story 3.1: Contact Management System

**As a** lead researcher  
**I want** to manage organization contacts and roles  
**So that** we can effectively target our outreach

**Development Tasks:**

1. Domain Layer:

   - Define Contact and Role models
   - Create contact management interfaces
   - Define role categorization rules

2. Infrastructure Layer:

   - Implement secure contact storage
   - Create role management system
   - Build contact validation service

3. API Layer:

   - Create contact management endpoints
   - Add role management endpoints
   - Implement contact search endpoints

4. Testing:
   - Contact validation tests
   - Role management tests
   - Security compliance tests

### Story 3.2: Engagement Tracking System

**As a** business analyst  
**I want** to track and measure engagement with organizations  
**So that** we can optimize our outreach efforts

**Development Tasks:**

1. Domain Layer:

   - Define Interaction and Engagement models
   - Create tracking interfaces
   - Define ROI calculation rules

2. Infrastructure Layer:

   - Implement interaction history system
   - Create engagement scoring service
   - Build ROI calculation engine

3. API Layer:

   - Add interaction tracking endpoints
   - Create engagement analysis endpoints
   - Implement ROI reporting endpoints

4. Testing:
   - Tracking accuracy tests
   - Engagement scoring tests
   - ROI calculation validation

## Definition of Done Checklist

Each story must complete this checklist following the development workflow:

1. Domain Implementation:

   - [ ] Domain models defined in `app/core/domain.py`
   - [ ] Core interfaces defined in `app/core/storage.py` or `app/core/model.py`
   - [ ] Business rules implemented and validated

2. Infrastructure Implementation:

   - [ ] Storage implementation complete
   - [ ] Services implemented in appropriate infrastructure modules
   - [ ] External integrations tested

3. API Implementation:

   - [ ] REST endpoints implemented
   - [ ] Input validation complete
   - [ ] Error handling implemented

4. Testing:

   - [ ] Unit tests for domain logic
   - [ ] Integration tests for infrastructure
   - [ ] API endpoint tests
   - [ ] Performance requirements met

5. Documentation:
   - [ ] API documentation updated
   - [ ] Implementation details documented
   - [ ] Usage examples provided
