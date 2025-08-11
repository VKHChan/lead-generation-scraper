from dataclasses import asdict, fields
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


class SearchProvider:
    """
    Represents a search provider.
    """
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"


class SearchResult(BaseModel):
    """
    Represents a search result from a web search engine.
    """
    title: str = Field(description="The title of the search result.")
    url: str = Field(description="The URL of the search result.")
    description: str = Field(
        description="The description of the search result.")
    created_at: datetime = Field(
        description="The date and time the job was created")
    source: str = Field(description="The source of the search result.")
    snippet: str | None = Field(
        description="The snippet of the search result.")


class ModelHost:
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    AWS = "aws"


class ModelProvider:
    ANTHROPIC = "anthropic"


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


@dataclass
class BaseSettings:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> list[str]:
        return [f.name for f in fields(cls)]


@dataclass(frozen=True)
class ChatModelSettings:
    host: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    streaming: bool = True
    force_tool_support: bool = False
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int | None = None


class ContentType:
    """
    Represents the type of content being analyzed.
    """
    COMPANY_BLOG = "company_blog"
    NON_PROFIT_RESOURCE_BLOG = "non_profit_resource_blog"
    PERSONAL_BLOG = "personal_blog"
    OTHER = "other"


class PainPointCategories:
    """
    Represents the categories of pain points.
    """
    FUNDRAISING_RELATIONS = "fundraising_and_donor_relations"
    GRANTS_AND_FUNDING_MANAGEMENT = "grants_and_funding_management"
    VOLUNTEER_AND_RECRUITMENT_MANAGEMENT = "volunteer_and_recruitment_management"
    PROGRAM_SERVICE_DELIVERY = "program_service_delivery"
    MARKETING_OUTREACH_AND_ENGAGEMENT = "marketing_outreach_and_engagement"
    FINANCE_ACCOUNTING_AND_COMPLIANCE = "finance_accounting_and_compliance"
    INTERNAL_OPERATIONS_AND_STAFF_PRODUCTIVITY = "internal_operations_and_staff_productivity"
    IMPACT_MEASUREMENT_AND_REPORTING = "impact_measurement_and_reporting"
    IT_AND_DATA_MANAGEMENT = "it_and_data_management"
    OTHER = "other"


class PainPointImpact:
    OTHER = "other"


class PainPoint(BaseModel):
    description: str
    category: str = Field(
        default=PainPointCategories.OTHER,
        description="Pain point category - one of: fundraising_and_donor_relations, grants_and_funding_management, volunteer_and_recruitment_management, program_service_delivery, marketing_outreach_and_engagement, finance_accounting_and_compliance, internal_operations_and_staff_productivity, impact_measurement_and_reporting, it_and_data_management, other (default)"
    )
    impact: str = Field(
        default=PainPointImpact.OTHER,
        description="Pain point impact - one of: other (default)"
    )
    source_quote: str
    solution: str | None = None


class ServiceProvider(BaseModel):
    name: str
    website: str | None
    value_proposition: str | None = None
    pain_points: list[PainPoint] | None = None


class ContentAnalysis(BaseModel):
    url: str
    title: str
    analysis_date: datetime
    content_type: str = Field(
        default=ContentType.OTHER,
        description="Content type - one of: company_blog, non_profit_resource_blog, personal_blog, other (default)"
    )
    service_providers: list[ServiceProvider] | None = None
