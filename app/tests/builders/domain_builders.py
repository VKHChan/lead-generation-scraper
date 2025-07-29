"""
Test data builders for domain models.

Following the Builder Pattern as specified in the technical design document.
These builders provide a clean, readable way to construct test data.
"""
from app.core.domain import Organization


class OrganizationBuilder:
    """
    Builder for Organization test data.

    Provides methods to create Organization instances with default values
    that can be overridden for specific test cases.
    """

    @staticmethod
    def build(**kwargs) -> Organization:
        """
        Build an Organization instance with default values.

        Args:
            **kwargs: Override any default values for specific test cases.

        Returns:
            Organization: A valid Organization instance.
        """
        default_data = {
            "name": "Test Nonprofit",
            "province": "Ontario",
            "city": "Toronto",
            "primary_cause": "Education",
            "charitable_registration_number": None,
            "staff_count": None,
            "volunteer_count": None,
            "annual_revenue": None,
            "website": None,
            "email": None,
            "phone": None
        }
        return Organization(**{**default_data, **kwargs})

    @classmethod
    def build_small(cls) -> Organization:
        """Build a small organization (less than 10 employees)."""
        return cls.build(staff_count=5)

    @classmethod
    def build_medium(cls) -> Organization:
        """Build a medium organization (10-50 employees)."""
        return cls.build(staff_count=25)

    @classmethod
    def build_large(cls) -> Organization:
        """Build a large organization (more than 50 employees)."""
        return cls.build(staff_count=100)

    @classmethod
    def build_with_full_contact(cls) -> Organization:
        """Build an organization with all contact information."""
        return cls.build(
            email="contact@example.org",
            phone="1234567890",
            website="https://example.org"
        )
