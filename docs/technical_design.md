# Technical Design and Architectural Guidelines

## 1. Introduction

This document provides a technical overview of the "Lead Generation Scraper" project's architecture, design patterns, and development conventions. It is intended to guide developers (both human and AI) to ensure consistency, maintainability, and quality in the codebase. All future development should adhere to these guidelines.

## 2. Core Architectural Philosophy

The system is built on the principles of **Clean Architecture** and **Domain-Driven Design (DDD)**. This is evident in the clear separation of concerns between different layers of the application, visible in the directory structure.

The primary goal of this architecture is to create a system that is:

- **Independent of Frameworks**: The core business logic is not tied to FastAPI or any web framework.
- **Testable**: Business rules can be tested without the UI, database, or any external element.
- **Independent of UI**: The UI can change easily without changing the rest of the system.
- **Independent of Database**: The core domain is not coupled to a specific database technology like PostgreSQL.

## 3. Directory Structure and Layering

The project follows a distinct layered architecture, with each layer having a specific responsibility.

- `app/core`: **Domain Layer**. This is the heart of the application. It contains the enterprise-wide business logic and data structures (e.g., `domain.py`, `storage.py`). This layer has **zero dependencies** on any other layer in the application.

- `app/db`: **Infrastructure/Data Layer**. This layer is responsible for data persistence. It provides concrete implementations of the repository interfaces defined in the core domain layer. It uses SQLAlchemy for ORM and Alembic for database migrations.

- `app/api`: **Application/API Layer**. This is the presentation layer, responsible for handling incoming HTTP requests and exposing the system's functionality via a REST API. It uses the FastAPI framework. This layer depends on the `core` and `infrastructure` layers but should not contain business logic.

- `app/infrastructure`: **Infrastructure/Services Layer**. This layer is responsible for initializing and wiring up the application's dependencies using the **Dependency Injection (DI)** pattern. It contains modules for setting up the database (`db_module.py`) and other modules and application services (`service_collection.py`).

- `app/configuration`: **Configuration Layer**. This layer manages application settings, separating them by environment (local, AWS, Azure).

## 4. Key Design Patterns

- **Repository Pattern**: Abstracting data access. The `core/repository.py` defines the interfaces for data access, and the `db` layer provides the concrete implementations. This decouples the domain logic from the persistence mechanism.

- **Dependency Injection (DI)**: Managing dependencies. The `injector` library is used to decouple components and make the application more modular and testable. Services and repositories are "injected" into the components that need them rather than being created internally.

## 5. Core Engineering Principles

Beyond the specific patterns, all development should adhere to the following fundamental software engineering principles:

- **Single Responsibility Principle (SRP)**: Each class, function, or module should have one, and only one, reason to change. For example, a repository's responsibility is data access, not business logic. An API endpoint's responsibility is handling HTTP requests and responses, not orchestrating complex workflows.

- **Don't Repeat Yourself (DRY)**: Avoid duplicating code. If you find yourself writing the same logic in multiple places, it's a signal to create a reusable function, class, or service to encapsulate that logic.

- **Design for Testability**: Write code that is easy to test. This means favoring pure functions, using dependency injection to provide mocks or stubs, and avoiding complex, untestable logic in constructors or private methods.

- **Abstract External Integrations**: Any integration with an external service (e.g., a payment gateway, a third-party API) must be placed behind an abstraction (an interface or port) defined in the `core` layer. The concrete implementation for that service will live in the `infrastructure` layer. This prevents the core business logic from being coupled to a specific vendor.

- **Keep It Simple, Stupid (KISS)**: Always prefer the simplest solution that effectively solves the problem. Avoid unnecessary complexity, over-engineering, or adding features that are not required by the current user story.

- **You Ain't Gonna Need It (YAGNI)**: Do not implement functionality on the assumption that you might need it in the future. Focus only on implementing what is required to satisfy the current acceptance criteria.

## 6. Testing Strategy

The project is set up for comprehensive testing, with a clear structure that mirrors the application's layers.

- **Unit Tests**: These should be the most numerous tests. They test individual components in isolation. For example, testing a domain entity's logic should not require a database or an API.
- **Integration Tests**: These tests verify the collaboration between components, such as testing the interaction between the API layer and the database layer.
- **Test Data Builders**: The `app/tests/builders` directory indicates a preference for the **Builder Pattern** to create test data. This approach provides a clean, readable, and maintainable way to construct complex domain objects for test scenarios (e.g., `domain_builders.py`). This is the preferred method for generating test fixtures.

## 7. Development Workflow

1.  **Spec-Driven Development**: As established, all new features or changes should begin with a high-level requirement and one or more user stories in the `specs` directory.
2.  **Domain First**: Implement changes to the domain objects in `app/core/domain.py` first.
3.  **Repository and UoW**: Update the repository and unit of work interfaces in the `core` layer if necessary. Each db model should have its own repository.
4.  **Database Implementation**: Implement any changes to the data layer in `app/db`, including new repository methods and database models. Create a new Alembic migration if the schema changes.
5.  **API Endpoints**: Create or modify the API endpoints in `app/api`.
6.  **Dependency Injection**: Wire up any new services or repositories in the `app/infrastructure` layer. Logically separate services and modules into different files.
7.  **Testing**: Write corresponding tests in the `app/tests` directory, following the established patterns.

By following these guidelines, we can ensure that the project remains well-structured, maintainable, and easy to extend over time.
