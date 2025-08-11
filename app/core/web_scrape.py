from core.domain import ScrapingResult


class WebScraper:

    async def scrape_multiple(self, urls: list[str], file_path: str = None) -> ScrapingResult:
        raise NotImplementedError
