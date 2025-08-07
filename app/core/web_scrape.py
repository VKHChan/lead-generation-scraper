from datetime import datetime

from pydantic import BaseModel, Field


class ScrapePageResult(BaseModel):
    url: str = Field(description="The URL to scrape")
    success: bool = Field(description="Whether the scraping was successful")
    created_at: datetime = Field(
        description="The date and time the job was created")
    title: str | None = Field(description="The title of the scraped page")
    content: str | None = Field(description="The content of the scraped page")
    error_message: str | None = Field(
        description="The error message if the scraping failed")


class ScrapingResult(BaseModel):
    total_requests: int = Field(
        description="The total number of requests made")
    successful_requests: int = Field(
        description="The number of successful requests")
    failed_requests: int = Field(
        description="The number of failed requests")
    failed_urls: list[str] = Field(
        description="The URLs that failed to be scraped")
    successful_urls: list[str] = Field(
        description="The URLs that were successfully scraped")


class WebScraper:

    async def scrape_multiple(self, urls: list[str]) -> ScrapingResult:
        raise NotImplementedError
