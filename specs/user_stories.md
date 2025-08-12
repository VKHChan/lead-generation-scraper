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

### Story 1.2: LLM-Based Content Analysis ✅

**As a** business analyst  
**I want** to use LLM to analyze each scraped article and extract structured insights  
**So that** we can build a database of pain points, solutions, and market opportunities

**Implemented Features:**

1. Domain Layer ✅

   - Defined content analysis models:

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
             source_quote: str
             context: str

         class Solution:
             name: str
             description: str
             target_pain_points: list[str]
             features: list[str]
             benefits: list[str]
             pricing_info: str | None

         class ServiceProvider:
             name: str
             website: str | None
             described_solutions: list[str]
             value_proposition: str
     ```

2. Infrastructure Layer ✅

   - Implemented LLM analysis pipeline:
     - Content extraction service
     - LLM prompt engineering
     - JSON response parsing and validation
   - Created storage structure:
     ```
     storage/
       └── YYYY/MM/DD/
           └── content/
               └── {url_hash}/
                   ├── raw.json
                   └── analysis.json
     ```

3. LLM Integration ✅

   - Implemented extraction prompt:
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
     ```
   - Added validation and error handling

### Story 1.3: Reddit Integration

**As a** business analyst  
**I want** to analyze Reddit discussions about non-profit operations  
**So that** we can validate pain points and discover new opportunities

**Development Tasks:**

1. Domain Layer:

   - Extend ContentAnalysis model for Reddit:

     ```python
     class RedditSource(ContentSource):
         subreddit: str
         post_id: str
         score: int
         comment_count: int

     class RedditAnalysis(ContentAnalysis):
         source: RedditSource
         community_sentiment: float
         validation_metrics: ValidationMetrics

         class ValidationMetrics:
             agreement_score: float
             discussion_depth: int
             solution_mentions: int
             similar_experiences: int
     ```

2. Infrastructure Layer:

   - Implement Reddit data collection:
     - Subreddit monitoring service
     - Post and comment fetching
     - Rate limiting compliance
   - Extend storage structure:
     ```
     storage/
       └── YYYY/MM/DD/
           └── content/
               ├── web/
               │   └── {url_hash}/
               └── reddit/
                   └── {subreddit}/
                       └── {post_id}/
     ```

3. Analysis Integration:

   - Extend LLM prompts for Reddit content:
     - Community sentiment analysis
     - Discussion validation metrics
     - Solution effectiveness scoring
   - Create aggregation tools:
     ```python
     async def aggregate_reddit_insights(
         start_date: date,
         end_date: date
     ) -> RedditInsights:
         """Aggregate Reddit analysis results"""
         return {
             'validated_pain_points': list[ValidatedPainPoint],
             'community_solutions': list[CommunitySolution],
             'trending_topics': list[TrendingTopic]
         }
     ```

4. Testing:
   - Reddit API integration tests
   - Content analysis adaptation tests
   - Insight aggregation validation

### Story 1.4: Non-profit Organization Profiling

**As a** lead researcher  
**I want** to build comprehensive profiles of Canadian non-profit organizations  
**So that** we can identify potential clients for our automation solutions

**Development Tasks:**

1. Domain Layer:

   - Define Organization model:

     ```python
     class Organization:
         """Non-profit organization profile"""
         name: str
         registration_number: str
         website: str | None
         location: Location
         size: OrgSize
         focus_areas: list[str]
         tech_profile: TechProfile
         identified_pain_points: list[str]  # References to ContentAnalysis
         contact_info: ContactInfo

         class TechProfile:
             tech_stack: list[str]
             online_presence: OnlinePresence
             automation_readiness: float
     ```

2. Infrastructure Layer:

   - Implement data collection services:
     - CRA data scraper
     - Website analyzer
     - Social media scanner
   - Create profile enrichment pipeline:
     - Tech stack detection
     - Digital presence analysis
     - Pain point matching
   - Build storage system:
     ```
     storage/
       └── organizations/
           └── {province}/
               └── {org_id}/
                   ├── profile.json
                   ├── tech_analysis.json
                   └── pain_points.json
     ```

3. Analysis Tools:

   - Create analysis utilities:
     ```python
     async def match_org_pain_points(
         org_id: str,
         content_analyses: list[ContentAnalysis]
     ) -> MatchResults:
         """Match organization profile with identified pain points"""
         return {
             'matching_points': list[PainPointMatch],
             'confidence_scores': list[float],
             'recommended_solutions': list[Solution]
         }
     ```

4. Testing:
   - Data collection accuracy
   - Profile enrichment validation
   - Pain point matching accuracy
   - Integration with content analysis system

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
