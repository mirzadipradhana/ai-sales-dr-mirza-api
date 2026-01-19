# AI Sales Doctor Lead Management API

A FastAPI-based REST API for lead management, built with Python 3.12+ and managed with `uv`.

## Features

- 🚀 FastAPI with async/await support
- 🔒 CORS middleware configured
- 📝 Interactive API documentation (Swagger/ReDoc)
- ⚙️ Environment-based configuration
- 🏥 Health check endpoint
- 📦 Dependency management with `uv` (no pip required)
- ☁️ Vercel deployment ready

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew
brew install uv

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

1. Navigate to the project directory:

   ```bash
   cd app
   ```
2. Install dependencies using `uv`:

   ```bash
   uv sync
   ```

   This will:

   - Create a virtual environment (if needed)
   - Install all dependencies from `pyproject.toml`
   - Use the lock file (`uv.lock`) for reproducible builds

## Running the Application

### Development Mode

From the parent directory (`ai-sales-dr-mirza-api`), run:

```bash
uv run --project app uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Production Mode

```bash
uv run --project app uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://127.0.0.1:8000

## API Endpoints

### Root Endpoint

- **GET** `/`
  - Returns API information including name, version, and available endpoints
  - **Response**:
    ```json
    {
      "name": "Lead Management API",
      "version": "1.0.0",
      "docs": "/docs",
      "health": "/health"
    }
    ```

### Health Check

- **GET** `/health`
  - Returns the health status of the API
  - **Response**:
    ```json
    {
      "status": "healthy",
      "version": "1.0.0",
      "environment": "development"
    }
    ```

## Project Structure

```
app/
├── core/
│   ├── config.py          # Application settings and configuration
│   └── exception.py        # Custom exception handlers
├── main.py                 # FastAPI application entry point
├── pyproject.toml          # Project dependencies and metadata
├── uv.lock                 # Locked dependency versions
├── vercel.json             # Vercel deployment configuration
└── README.md               # This file
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the `app/` directory:

```env
# Application
APP_NAME=Lead Management API
VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# API
API_V1_PREFIX=/api/v1

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

All settings have sensible defaults defined in `core/config.py`.

## Development

### Installing Dev Dependencies

```bash
uv sync --extra dev
```

### Code Formatting

```bash
# Format code with Black
uv run black .

# Lint with Ruff
uv run ruff check .
uv run ruff format .
```

### Running Tests

```bash
uv run pytest
```

## Deployment

### Vercel

The project is configured for Vercel deployment. The `vercel.json` file handles routing and the `handler = app` in `main.py` exposes the FastAPI app to Vercel's serverless functions.

Deploy using:

```bash
vercel
```

## Dependencies

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation using Python type annotations
- **Pydantic Settings** - Settings management using Pydantic models
- **Python-dotenv** - Load environment variables from `.env` files
- **Faker** - Generate fake data for testing
- **Python-multipart** - Support for form data

## License

MIT

## Author

Mirza Dipradhana - madipradhana@gmail.com
