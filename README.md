# Market Research and Lead Generation Tool

A Python-based tool that combines web search, content scraping, and AI analysis to:

1. Research market opportunities and pain points
2. Analyze existing solutions and service providers
3. Generate qualified leads based on market fit

## Features

### Data Collection

- Automated web search using DuckDuckGo
- Smart web scraping with retry logic and error handling
- Hierarchical storage system (local/S3 compatible)
- Rate limiting and robots.txt compliance

### Content Analysis

- AI-powered content analysis using LLM
- Extraction of:
  - Pain points and operational challenges
  - Existing solutions and their features
  - Service providers and their offerings
- Source tracking with original quotes and context

### Market Intelligence

- Pain point frequency analysis
- Solution landscape mapping
- Provider market share insights
- Opportunity gap identification

## Project Structure

```
lead-generation-scraper/
├── app/
│   ├── core/           # Domain models and business logic
│   │   ├── web_search.py    # Search interfaces
│   │   └── web_scrape.py   # Scraping interfaces
│   ├── infrastructure/ # Service implementations
│   │   ├── web_search_services.py
│   │   └── web_scrape_services.py
│   ├── configuration/  # Settings and configuration
│   └── tests/         # Test suites
├── storage/           # Data storage
│   └── YYYY/MM/DD/    # Hierarchical data organization
└── specs/
    ├── high_level_requirements.md
    └── user_stories.md # Project requirements
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/VKHChan/lead-generation-scraper.git
   cd lead-generation-scraper
   ```

2. Create and configure environment:

   ```bash
   cp .env_sample .env
   # Edit .env with your settings
   ```

3. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

4. Run a search:
   ```bash
   python -m app.main "your search query"
   ```

## Configuration (.env)

see [`.env.sample`](.env.sample)

## Development

The project is developed in phases:

1. **Data Collection** ✅

   - Web search integration
   - Content scraping
   - Structured storage

2. **Content Analysis** 🚧

   - LLM-based analysis
   - Entity extraction
   - Pattern recognition

3. **Market Intelligence** 📅
   - Trend analysis
   - Gap identification
   - Lead scoring

## License

MIT License
