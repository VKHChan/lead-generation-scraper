"""
Unit tests for domain models.

Following the testing strategy outlined in the technical design document.
Tests are organized by domain entity and cover both validation and behavior.
"""
from datetime import datetime

import pytest

from app.core.domain import Organization, OrganizationSize
from app.tests.builders.domain_builders import OrganizationBuilder


class TestOrganization:
    """
    Test cases for the Organization domain model.

    Following DDD principles, tests focus on maintaining domain invariants
    and business rules.
    """

    def test_valid_organization_creation(self):
        """Test creating a valid organization with all fields."""
        org = OrganizationBuilder.build(
            charitable_registration_number="12345",
            staff_count=5,
            volunteer_count=20,
            annual_revenue=100000.0,
            website="https://example.org",
            email="contact@example.org",
            phone="1234567890"
        )
        assert org.name == "Test Nonprofit"
        assert org.province == "Ontario"
        assert isinstance(org.created_at, datetime)

    def test_required_fields_validation(self):
        """Test validation of required fields."""
        # Test missing name
        with pytest.raises(ValueError, match="Organization name is required"):
            OrganizationBuilder.build(name="")

        # Test missing province
        with pytest.raises(ValueError, match="Province is required"):
            OrganizationBuilder.build(province="")

    def test_email_validation(self):
        """Test email format validation."""
        # Test invalid email
        with pytest.raises(ValueError, match="Invalid email format"):
            OrganizationBuilder.build(email="invalid-email")

        # Test valid email
        org = OrganizationBuilder.build(email="valid@example.com")
        assert org.email == "valid@example.com"

    def test_website_validation(self):
        """Test website format validation."""
        # Test invalid website
        with pytest.raises(ValueError, match="Invalid website format"):
            OrganizationBuilder.build(website="not-a-url")

        # Test valid website
        org = OrganizationBuilder.build(website="https://example.org")
        assert org.website == "https://example.org"

    def test_numeric_validation(self):
        """Test validation of numeric fields."""
        # Test negative staff count
        with pytest.raises(ValueError, match="Staff count cannot be negative"):
            OrganizationBuilder.build(staff_count=-1)

        # Test negative volunteer count
        with pytest.raises(ValueError, match="Volunteer count cannot be negative"):
            OrganizationBuilder.build(volunteer_count=-1)

    def test_size_category_behavior(self):
        """Test organization size categorization behavior."""
        # Test different size categories
        assert OrganizationBuilder.build_small().get_size_category() == OrganizationSize.SMALL
        assert OrganizationBuilder.build_medium(
        ).get_size_category() == OrganizationSize.MEDIUM
        assert OrganizationBuilder.build_large().get_size_category() == OrganizationSize.LARGE

        # Test None case
        org_no_staff = OrganizationBuilder.build(staff_count=None)
        assert org_no_staff.get_size_category() is None

    def test_update_contact_info_behavior(self):
        """Test contact information update behavior."""
        org = OrganizationBuilder.build()

        # Test valid updates
        org.update_contact_info(
            email="new@example.com",
            phone="1234567890",
            website="https://new.example.org"
        )
        assert org.email == "new@example.com"
        assert org.phone == "1234567890"
        assert org.website == "https://new.example.org"

        # Test invalid email update
        with pytest.raises(ValueError, match="Invalid email format"):
            org.update_contact_info(email="invalid-email")
