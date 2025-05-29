# Atlas Provider for SQLAlchemy - Development Guide

This document provides instructions for developers who want to contribute to or modify the `atlas-provider-sqlalchemy` project.

## Project Overview

`atlas-provider-sqlalchemy` is a tool that bridges [SQLAlchemy](https://www.sqlalchemy.org/) (a Python SQL toolkit and ORM) with [Atlas](https://atlasgo.io) (a database schema management tool). It allows users to:

1. Export SQLAlchemy model definitions as SQL DDL statements
2. Use Atlas to plan and apply migrations based on SQLAlchemy models
3. Automatically create migration files from SQLAlchemy model changes

## Development Setup

### Prerequisites

- Python 3.9 or newer
- [Poetry](https://python-poetry.org/) for dependency management
- [Atlas CLI](https://atlasgo.io/getting-started#installation)

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd atlas-provider-sqlalchemy
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install --all-extras
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Project Structure

- `atlas_provider_sqlalchemy/` - Main package
  - `ddl.py` - Core functionality for extracting schema information from SQLAlchemy models
  - `main.py` - CLI interface using Typer
- `tests/` - Test fixtures and test cases
  - `models/` - Example SQLAlchemy models for testing
  - `migrations/` - Sample migration files

## Development Workflow

### Running Tests

Run the test suite using `pytest` at the root of the project directory. This will execute all tests defined in the `tests/` directory:

```bash
pytest
```

Or, to run tests across multiple Python versions:

```bash
tox
```

### Running Integration Tests With Atlas
To run integration tests, ensure you have a running database instance (e.g., MySQL, PostgreSQL) and set the appropriate environment variables. Then execute:

Standalone Mode:
```bash
cd tests
atlas schema inspect -c "file://atlas-standalone.hcl" --env sqlalchemy  --var dialect={dialect} --url "env://src"
```

As a Python script:
```bash
cd tests
atlas schema apply -c "file://atlas-script.hcl" --env sqlalchemy --var dialect={dialect} --url "env://src"
```

### Vscode Configuration for debugging

To set up debugging in Visual Studio Code, create a `.vscode/launch.json` file with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug Atlas Provider",
            "type": "python",
            "request": "launch",
            "module": "atlas_provider_sqlalchemy.main",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

and a `.vscode/settings.json` file with the following content to configure testing:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}"
    ]
}
```

> Choose the appropriate Python interpreter in VSCode that matches your Poetry environment.