## 6. Testing Strategy

The project is set up for comprehensive testing, with a clear structure that mirrors the application's layers.

- **Unit Tests**: These should be the most numerous tests. They test individual components in isolation. For example, testing a domain entity's logic should not require a database or an API.
- **Integration Tests**: These tests verify the collaboration between components, such as testing the interaction between the API layer and the database layer.
- **Test Data Builders**: The `app/tests/builders` directory indicates a preference for the **Builder Pattern** to create test data. This approach provides a clean, readable, and maintainable way to construct complex domain objects for test scenarios (e.g., `domain_builders.py`). This is the preferred method for generating test fixtures.

### Test Builder Pattern Example: OrganizationBuilder

The Test Builder pattern is a design pattern that helps create test objects in a more maintainable and readable way. Here's why we use it:

1. Problem Without Builder:

```python
# Without builder, creating test objects is verbose and repetitive
def test_something():
    org1 = Organization(
        name="Test Org",
        province="Ontario",
        city="Toronto",
        primary_cause="Education",
        charitable_registration_number=None,
        staff_count=None,
        volunteer_count=None,
        annual_revenue=None,
        website=None,
        email=None,
        phone=None
    )

    org2 = Organization(
        name="Test Org",
        province="Ontario",
        city="Toronto",
        primary_cause="Education",
        charitable_registration_number=None,
        staff_count=5,  # only this is different
        volunteer_count=None,
        annual_revenue=None,
        website=None,
        email=None,
        phone=None
    )
```

2. Solution With Builder:

```python
def test_something():
    # Much cleaner - only specify what's different from defaults
    org1 = OrganizationBuilder.build()
    org2 = OrganizationBuilder.build(staff_count=5)
```

Let's look at our builder in detail:

```python
class OrganizationBuilder:
    @staticmethod
    def build(**kwargs) -> Organization:
        """
        Build an Organization instance with default values.
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
```

#### Key benefits:

1. Default Values:

```python
   # All default values handled by builder
   org = OrganizationBuilder.build()
```

2. Override Specific Values:

```python
   # Only specify what's different
   org = OrganizationBuilder.build(
       name="Custom Name",
       email="test@example.com"
   )
```

3. Common Test Scenarios:

```python
   # Pre-configured scenarios
   small_org = OrganizationBuilder.build_small()
   medium_org = OrganizationBuilder.build_medium()
```

4. Maintainability:
   If we add a new required field to Organization, we only update the builder's default_data
   All tests automatically get the new field's default value

5. Readability:

```python
   # Clear intent of test
   def test_size_categories():
       small = OrganizationBuilder.build_small()
       medium = OrganizationBuilder.build_medium()
       large = OrganizationBuilder.build_large()
```

6. Encapsulation of Test Data:
   Test data creation logic is centralized
   Changes to test data patterns only need to be made in one place
