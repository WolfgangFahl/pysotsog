# Agent Guidelines for pysotsog

This document provides instructions for AI agents operating in the `pysotsog` repository.

## 1. Build, Test, and Lint Commands

The project uses `unittest` for testing and custom shell scripts for common tasks located in the `scripts/` directory.

### Running Tests
The primary script for running tests is `scripts/test`. It supports various modes:

- **Run all tests (Standard):**
  ```bash
  ./scripts/test
  ```
  This runs `python3 -m unittest discover`.

- **Run all tests (with Green):**
  If `green` is installed, this provides colored output and parallel execution options.
  ```bash
  ./scripts/test -g
  ```

- **Run a single test module:**
  Use this when working on a specific feature to save time.
  ```bash
  python3 -m unittest tests/test_sotsog.py
  ```

- **Run a specific test case:**
  Target a specific method within a test class.
  ```bash
  python3 -m unittest tests.test_sotsog.TestSotsog.test_sotsog_search
  ```
  *(Note: Adjust the path and class name according to the file you are testing)*

- **Run tests module-by-module:**
  This is useful for isolating failures when the global test runner crashes or hangs.
  ```bash
  ./scripts/test -m
  ```

### Installation
- **Install the package in editable mode (or update):**
  ```bash
  ./scripts/install
  ```
  *(This runs `pip install . -U`)*

- **Install and run tests:**
  A convenience script to ensure environment is up-to-date before testing.
  ```bash
  ./scripts/installAndTest
  ```

### Linting & Formatting
The project enforces code style using `black` and `isort`.
- **Format code:**
  ```bash
  ./scripts/blackisort
  ```
  *Agents should run this script before submitting changes to ensure compliance with project formatting.*

## 2. Code Style & Conventions

### General
- **Language:** Python 3.10+
- **Style:** Adhere to PEP 8, enforced by `black` and `isort`.
- **Type Hinting:** Use standard Python type hints for function arguments and return values.
  ```python
  from argparse import ArgumentParser
  
  def getArgParser(self, description: str, version_msg: str) -> ArgumentParser:
      ...
  ```

### Imports
- **Ordering:** Standard library first, then third-party libraries, then local imports.
- **Sorting:** Managed by `isort`. Run `./scripts/blackisort` to fix imports automatically.
- **Local Imports:** Use absolute imports where possible (e.g., `from skg.sotsog import SotSog` instead of `from .sotsog import SotSog`).

### Docstrings
- **Format:** Use multi-line strings for module, class, and function docstrings.
- **Metadata:** Include creation date and author tags in module docstrings.
  ```python
  """
  Created on 2024-02-26

  @author: wf
  """
  ```
- **Content:** Briefly explain the purpose of the class or function.
- **Classes:** Docstring should describe the class's responsibility.
- **Methods:** Docstring should describe what the method does, its arguments, and return value if complex.

### Naming
- **Classes:** `CamelCase` (e.g., `SotSog`, `SkgBrowser`)
- **Functions/Methods:** `snake_case` (e.g., `handle_args`, `get_config`)
- **Variables:** `snake_case` (e.g., `exit_code`, `search_results`)
- **Constants:** `UPPER_CASE` (e.g., `DEBUG`, `MAX_RETRIES`)

### Error Handling
- Use specific exceptions where possible (e.g., `ValueError` instead of `Exception`).
- Wrap network calls or external API interactions in try-except blocks, especially when dealing with web scraping or external services.
- Log errors appropriately if a logging framework is available (check `pybasemkit`).

## 3. Project Structure

- **`skg/`**: Main package source code ("Standing on the shoulders of giants").
  - `sotsog_cmd.py`: Command-line interface entry point.
  - `sotsog.py`: Main logic for the search engine/browser.
  - `__init__.py`: Version definition.
- **`tests/`**: Unit tests.
  - Tests should inherit from `basemkit.basetest.Basetest`.
  - Naming convention: `test_*.py`.
- **`scripts/`**: Helper shell scripts for building, testing, and formatting.
  - `test`: Main test runner.
  - `blackisort`: Formatter.
  - `install`: Installer.
- **`pyproject.toml`**: Project configuration and dependencies.
- **`sotsog_examples/`**: Example scripts or data.

## 4. Testing Guidelines

- **Framework:** `unittest`.
- **Base Class:** Use `Basetest` from `basemkit.basetest`.
  ```python
  from basemkit.basetest import Basetest

  class TestMyFeature(Basetest):
      def setUp(self):
          super().setUp()
          # Your setup code here

      def test_something(self):
          """
          Test description
          """
          # Your test code here
  ```
- **Debugging:** `Basetest` provides a `self.debug` flag. Use it to conditionally print debug info.
  ```python
  if self.debug:
      print(f"Debug info: {value}")
  ```
- **Coverage:** Aim to cover new features or bug fixes with a corresponding test case in `tests/`.
- **Output:** Avoid `print` statements in production code. Use them in tests only when `self.debug` is True.

## 5. Agent Behavior

- **Safety First:** Always analyze the code structure before making changes. Read files to understand context.
- **Dependencies:** Do not add new dependencies without checking `pyproject.toml` first. If adding one is necessary, update `pyproject.toml` under `dependencies`.
- **Verification Loop:**
  1.  **Analyze:** specific files using `read`.
  2.  **Plan:** your changes.
  3.  **Edit:** Apply changes.
  4.  **Format:** Run `./scripts/blackisort`.
  5.  **Test:** Run `./scripts/test` (or specific module) to verify changes.
- **Refactoring:** When refactoring, ensure existing tests pass before and after changes.
- **Documentation:** Update docstrings if you modify function signatures.
