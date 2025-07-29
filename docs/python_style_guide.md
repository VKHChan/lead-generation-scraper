# Python Style Guide and Coding Conventions

## 1. Introduction

This document outlines the specific coding conventions and style preferences for Python code in this project. The goal is to maintain a clean, consistent, and modern codebase. All developers and AI agents are expected to adhere to these guidelines.

These rules supplement the automated formatting provided by `black` and `isort`.

## 2. Modern Python Syntax

We prefer modern Python syntax where possible.

### 2.1. Type Hinting (PEP 585 & PEP 604)

- **Use Union Type Operator:** For optional types or unions, use the `|` operator (available in Python 3.10+) instead of `typing.Union` or `typing.Optional`.

  ```python
  # Preferred
  def process_data(data: str | None):
      ...

  # Not Preferred
  from typing import Optional
  def process_data(data: Optional[str]):
      ...
  ```

- **Use Standard Generic Types:** For collections, use the lowercase built-in types (`list`, `dict`, `set`) as generics (available in Python 3.9+) instead of their `typing` module equivalents (`List`, `Dict`, `Set`).

  ```python
  # Preferred
  def get_users() -> list[str]:
      ...

  # Not Preferred
  from typing import List
  def get_users() -> List[str]:
      ...
  ```

### 2.2. Dataclasses

- **Prefer Dataclasses for Data Structures:** For simple data-holding objects, prefer using `@dataclass` from the `pydantic.dataclasses` module (as established in the project) over plain classes. This reduces boilerplate and provides useful methods out of the box.

## 3. General Conventions

- **F-strings for Formatting:** Always use f-strings for string formatting unless the logging module's deferred formatting is more appropriate.

  ```python
  # Preferred
  name = "World"
  greeting = f"Hello, {name}!"

  # Not Preferred
  greeting = "Hello, {}!".format(name)
  greeting = "Hello, %s!" % name
  ```

- **Underscore for Unused Variables:** If a variable is intentionally unused (e.g., in a tuple unpacking), name it `_`.

  ```python
  # Preferred
  name, _ = get_user_and_token()
  ```
