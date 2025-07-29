# Definition of Done (DoD)

## 1. Introduction

This document defines the criteria that must be met for a user story to be considered "done". It serves as a checklist to ensure that every feature is developed with a consistent level of quality, testing, and documentation. No story can be considered complete until all applicable items on this list have been satisfied.

This DoD applies to all user stories developed for this project and should be used as a final quality gate by any developer, whether human or AI.

## 2. The Checklist

A user story is considered **done** only when it meets all of the following criteria:

-   [ ] **Code Complete**: All required code has been written to satisfy the user story's requirements.

-   [ ] **Acceptance Criteria Met**: All acceptance criteria outlined in the user story are fully implemented and have been verified.

-   [ ] **Adheres to Technical Design**: The implementation is fully compliant with the guidelines specified in the `docs/technical_design.md` document. This includes following the layered architecture, using the prescribed design patterns (Repository, Unit of Work, DI), and adhering to the established development workflow.

-   [ ] **Unit Tests Passed**: Comprehensive unit tests have been written for the new functionality, covering business logic, edge cases, and potential failures. All unit tests for the entire application must pass.

-   [ ] **Integration Tests Passed**: Integration tests have been written to verify the interaction between the new code and other parts of the system (e.g., API layer to database). All integration tests must pass.

-   [ ] **Code Quality and Formatting**: The code adheres to the project's quality standards, verified by ensuring the following commands run without errors:
    -   `black .`
    -   `isort . --profile black`
    -   `pyright app`

-   [ ] **Database Migration Created**: If the database schema was changed (e.g., adding a table or modifying a column), a new, correctly implemented Alembic migration script has been created in `app/db/versions`.

-   [ ] **API Documentation Updated**: If any API endpoints were added or modified, the automatically generated OpenAPI/Swagger documentation (via FastAPI) is accurate and reflects the changes.

-   [ ] **Application Runs Successfully**: The application can be started without runtime errors. This is verified by:
    -   Successfully running the application startup command as specified in the `README.md`: `fastapi dev app/main.py --port 7500`.
    -   Performing an automated smoke test by hitting the health check endpoint (`GET /health`) and receiving a successful response, as detailed in the `README.md` section "Verifying the API is Running". This must account for the configured authentication method.

## 3. How to Use This Document

Before marking a user story as complete, the developer must review this checklist and confirm that every item has been addressed. This ensures a shared understanding of quality and completeness across the entire team.
