"""
Domain models for the lead generation scraper.

This module contains the core domain models following DDD principles.
No external dependencies except for pydantic for data validation.
"""
import re
from datetime import datetime
from enum import Enum

from pydantic.dataclasses import dataclass


class OrganizationSize(Enum):
    """Organization size categories based on staff count."""
    SMALL = "small"      # < 10 employees
    MEDIUM = "medium"    # 10-50 employees
    LARGE = "large"      # > 50 employees


@dataclass
class Organization:
    """
    Core domain entity representing a non-profit organization.

    Implements validation rules and business logic for organization data.
    Following DDD principles, this entity maintains its own invariants.
    """
    name: str
    charitable_registration_number: str | None
    province: str
    city: str
    staff_count: int | None
    volunteer_count: int | None
    annual_revenue: float | None
    primary_cause: str
    website: str | None
    email: str | None
    phone: str | None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def __post_init__(self):
        """Validate the organization data after initialization."""
        self._validate_required_fields()
        self._validate_formats()
        self._validate_numbers()

    def _validate_required_fields(self) -> None:
        """Validate that required fields are not empty."""
        if not self.name:
            raise ValueError("Organization name is required")
        if not self.province:
            raise ValueError("Province is required")
        if not self.city:
            raise ValueError("City is required")
        if not self.primary_cause:
            raise ValueError("Primary cause is required")

    def _validate_formats(self) -> None:
        """Validate format of fields like email, phone, website."""
        if self.email and not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")
        if self.website and not self._is_valid_url(self.website):
            raise ValueError(f"Invalid website format: {self.website}")
        if self.phone and not self._is_valid_phone(self.phone):
            raise ValueError(f"Invalid phone format: {self.phone}")

    def _validate_numbers(self) -> None:
        """Validate numeric fields."""
        if self.staff_count is not None and self.staff_count < 0:
            raise ValueError("Staff count cannot be negative")
        if self.volunteer_count is not None and self.volunteer_count < 0:
            raise ValueError("Volunteer count cannot be negative")
        if self.annual_revenue is not None and self.annual_revenue < 0:
            raise ValueError("Annual revenue cannot be negative")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$'
        return bool(re.match(pattern, url))

    @staticmethod
    def _is_valid_phone(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))

    def get_size_category(self) -> OrganizationSize | None:
        """Determine organization size category based on staff count."""
        if self.staff_count is None:
            return None
        if self.staff_count < 10:
            return OrganizationSize.SMALL
        if self.staff_count < 50:
            return OrganizationSize.MEDIUM
        return OrganizationSize.LARGE

    def update_contact_info(
        self,
        email: str | None = None,
        phone: str | None = None,
        website: str | None = None
    ) -> None:
        """Update contact information with validation."""
        if email:
            if not self._is_valid_email(email):
                raise ValueError(f"Invalid email format: {email}")
            self.email = email
        if phone:
            if not self._is_valid_phone(phone):
                raise ValueError(f"Invalid phone format: {phone}")
            self.phone = phone
        if website:
            if not self._is_valid_url(website):
                raise ValueError(f"Invalid website format: {website}")
            self.website = website
        self.updated_at = datetime.now()
