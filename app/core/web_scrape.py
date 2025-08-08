from app.core.domain import ScrapingResult


class WebScraper:

    async def scrape_multiple(self, urls: list[str]) -> ScrapingResult:
        raise NotImplementedError
