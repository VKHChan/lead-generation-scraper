# Lead Generation Scraper

A Python-based web scraping application designed to collect and analyze automation needs data from Canadian non-profit organizations. The system provides a RESTful API for data access and automated weekly data collection.

## Features

- Automated web scraping of Canadian non-profit organizations
- Data collection from multiple sources (CRA, CharityVillage, etc.)
- RESTful API for data access
- Configurable storage backend (local CSV with cloud storage support)
- Weekly scheduled data collection
- Deduplication and data validation
- Rate limiting and robots.txt compliance

## Project Structure

```
lead-generation-scraper/
├── app/
│   ├── core/           # Domain models and business logic
│   ├── api/            # API endpoints
│   ├── infrastructure/ # Storage and external services
│   └── db/            # Database/storage implementations
├── docs/
│   ├── technical_design.md
│   ├── definition_of_done.md
│   └── python_style_guide.md
└── specs/
    ├── high_level_requirements.md
    └── user_stories.md
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/VKHChan/lead-generation-scraper.git
   cd lead-generation-scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

3. Run the application:
   ```bash
   fastapi dev app/main.py --port 7500
   ```

## API Documentation

The API provides the following endpoints:

- `POST /api/v1/scrape` - Initiate a new scraping job
- `GET /api/v1/scrape/status/{jobId}` - Get job status
- `GET /api/v1/leads` - Retrieve scraped leads
- `GET /api/v1/leads/{leadId}` - Get specific lead details

For detailed API documentation, visit the OpenAPI documentation at `/docs` when running the application.

## Development

Please refer to the following documentation before contributing:

- [Technical Design](docs/technical_design.md)
- [Definition of Done](docs/definition_of_done.md)
- [Python Style Guide](docs/python_style_guide.md)

## License

MIT License 