# Development Plan

This guide will help you quickly understand our code base and get started with making changes. Our code is organized in the `src/` directory with unit tests in `tests/`. Below is an overview and step-by-step instructions for setting up your environment, understanding key components, and running tests.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Environment Setup](#environment-setup)
- [Code Base Plan](#code-base-plan)
- [Making Changes](#making-changes)
- [Running the Service](#running-the-service)
- [Running Unit Tests](#running-unit-tests)
- [Getting Help](#getting-help)

---

## Project Overview

Managed EventBus is a simple, gRPC-based event queuing bus for Python, designed as a "Kafka‑lite" alternative. It is built with a modular architecture that includes:

- **Entry point (main.py):** Initializes the service and integrates core modules.
- **Configuration (config.yaml):** A central file that controls tuning parameters such as retention, batching, compression, and settings for persistence and queue.
- **Dynamic Plugin Loading (plugin_loader.py):** Loads pluggable components based on settings in `config.yaml`.
- **Core Processing (processing.py):** Contains business logic for processing events.
- **In-memory Queue (queue.py):** Implements queuing and retry logic.
- **Security Middleware (middleware.py):** Provides security via JWT validation and TLS.
- **Unit Tests (tests/):** Contains tests to ensure that modules work as expected (e.g., `test_plugin_loader.py`).

---

## Environment Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/salestracker/eventbus.git
   cd eventbus
   ```

2. **Install Dependencies:**
   We use [Poetry](https://python-poetry.org/) for dependency management.
   ```bash
   poetry install
   ```

3. **Set Up Your Environment Variables:**
   Configure any necessary environment variables (e.g., for database DSN, JWT secrets). You can use a `.env` file if needed.

4. **Optional: Set Up a Virtual Environment:**
   If you prefer not using Poetry's virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   poetry install
   ```

---

## Code Base Plan

### `src/` Directory

- **main.py:**  
  - **Role:** Entry point of the service.
  - **Details:** Initializes core modules, loads configuration, and starts the gRPC server.
  - **Tip:** When making changes here, ensure that the initialization sequence remains intact.

- **config.yaml:**  
  - **Role:** Centralized configuration file.
  - **Details:** Specifies tuning parameters such as event retention, batching, compression, persistence type, and queue settings.
  - **Tip:** Modify this file to experiment with different configurations. Changes here affect plugin loading and service behavior.

- **plugin_loader.py:**  
  - **Role:** Dynamically loads pluggable components.
  - **Details:** Reads `config.yaml` to determine which persistence or queue module to load.
  - **Tip:** When adding a new plugin, update this file if necessary and add details to `config.yaml`.

- **processing.py:**  
  - **Role:** Core event processing logic.
  - **Details:** Contains functions that process individual events.
  - **Tip:** Use simple “hello world” logic to test your changes before integrating complex business rules.

- **queue.py:**  
  - **Role:** In-memory event queuing and retry mechanism.
  - **Details:** Implements a simple queue using Python’s `deque` and uses retry mechanisms via the `tenacity` library.
  - **Tip:** Ensure that changes do not break the queue’s ability to reliably process and requeue events.

- **middleware.py:**  
  - **Role:** Provides security middleware.
  - **Details:** Contains JWT validation and TLS setup to secure gRPC endpoints.
  - **Tip:** When working on security features, always run tests to ensure no endpoints become inaccessible.

### `tests/` Directory

- **General Purpose:**
  - Contains unit tests for validating functionality.
  - **Example:** `test_plugin_loader.py` tests that plugins are correctly loaded from the configuration.
  - **Tip:** Run tests frequently during development to catch regressions early.

---

## Making Changes

1. **Identify the Feature or Bug:**
   - Read the corresponding feature description or bug report.
   - Locate the relevant file(s) in `src/` (e.g., if it's a configuration issue, check `config.yaml` and `plugin_loader.py`).

2. **Modify the Code:**
   - Make your changes, following the architectural pattern of separation of concerns.
   - Keep changes simple, “hello world” style when prototyping.

3. **Add or Update Unit Tests:**
   - Ensure that new functionality is covered under `tests/`.
   - Run tests locally before committing.

4. **Commit and Push:**
   - Write clear commit messages.
   - Create a pull request for review.

---

## Running the Service

Use the following command to run the service locally:

```bash
make run
```

This command uses the Makefile provided in the repository. It sets up the environment, runs `main.py`, and starts the gRPC server.

---

## Running Unit Tests

Run all unit tests with:

```bash
make test
```

This command triggers the test suite (using `pytest`) to validate that all modules are working as expected.

---