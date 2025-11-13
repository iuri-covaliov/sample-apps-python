# Python Sample App: Barebones

## Application Overview

This barebones application demonstrates a **DummyApp** - a simple long-running application that showcases fundamental Python application patterns including configuration management, logging, dependency injection, and graceful application lifecycle.

## Core Components

### DummyApp Features

The **DummyApp** (`app/core/dummy_app.py`) is a demonstration application that:

- **Displays a welcome banner** with configurable app name, version, and description
- **Performs sample calculations** using a built-in calculator service (addition, subtraction, multiplication, division)
- **Logs all operations** using structured logging with configurable levels and formats
- **Runs continuously** as a long-running process until manually stopped
- **Uses dependency injection** through the AppContext pattern for clean separation of concerns

### Calculator Service

The app includes a **Calculator service** (`app/services/calculator.py`) that:
- Provides basic mathematical operations (add, subtract, multiply, divide)
- Includes input validation and error handling
- Demonstrates service-layer architecture patterns
- Supports both integer and floating-point operations

### Application Context Pattern

The **AppContext** (`app/core/appcontext.py`) provides:
- Centralized configuration management through Pydantic Settings
- Structured logging setup with configurable formats
- Dependency injection container for services
- Clean separation between configuration, logging, and business logic

## How to Use the DummyApp

### Quick Start
```bash
# Install dependencies
make deps

# Run the application
make run
# or
uv run -m app.main
```

### What You'll See
When you run the app, it will:

1. **Initialize** - Set up logging and configuration
2. **Display welcome banner** - Shows app name, version, and description
3. **Perform calculations** - Executes sample math operations and logs results
4. **Enter run loop** - Keeps running until stopped with `Ctrl+C`

### Sample Output
```
Initializing application context...
[INFO|main|line:18] 2025-11-13 12:00:00: Application context initialized.
[INFO|main|line:40] 2025-11-13 12:00:00: Performing sample calculations...
[INFO|dummy_app|line:40] 2025-11-13 12:00:00: Addition: 15
[INFO|dummy_app|line:41] 2025-11-13 12:00:00: Subtraction: 5
[INFO|dummy_app|line:42] 2025-11-13 12:00:00: Multiplication: 50
[INFO|dummy_app|line:43] 2025-11-13 12:00:00: Division: 2.0

=======================================================
Welcome to Sample Python App v0.1.0!
I am your dummy application.
Description: Python App Barebones

I will not listen to any pert.
I will do absolutely nothing until you shut me down.
Use ctrl+c to exit.
=======================================================
```

### Customization

You can customize the application behavior through environment variables:

```bash
# .env file
APP_NAME="My Custom App"
APP_VERSION="1.0.0"
APP_DESCRIPTION="Custom description here"
LOGGING_LEVEL="DEBUG"
```

### Stopping the Application

The DummyApp runs continuously. To stop it:
- **Terminal**: Press `Ctrl+C`
- **Docker**: `docker compose down`
- **Background process**: Use `kill` command with the process ID

## Architecture Highlights

This barebones application demonstrates several important patterns:

- **Configuration Management**: Environment-based settings with Pydantic
- **Dependency Injection**: Clean separation of concerns through AppContext
- **Structured Logging**: Configurable logging with proper formatting
- **Service Layer**: Calculator service shows clean business logic separation
- **Application Lifecycle**: Proper initialization, execution, and shutdown handling
- **Testing Strategy**: Comprehensive test coverage with proper mocking patterns
