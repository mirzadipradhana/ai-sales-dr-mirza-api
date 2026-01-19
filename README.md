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

- **Development API**: http://127.0.0.1:8000
- **Staging API (Vercel)**: https://ai-sales-dr-mirza-api.vercel.app/

## API Endpoints

### Root Endpoint

- **GET** `/`
  - Returns API information including name and version
  - **Response**:
    ```json
    {
      "name": "Lead Management API",
      "version": "1.0.0"
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

### Leads Endpoints

All lead endpoints are prefixed with `/api/v1/leads`.

#### Create Lead

- **POST** `/api/v1/leads`
  - Creates a new lead in the system
  - **Request Body**:
    ```json
    {
      "name": "John Doe",
      "job_title": "CEO",
      "company": "Acme Corp",
      "email": "john.doe@acme.com",
      "industry": "Technology",
      "phone_number": "+1-555-0123",
      "headcount": 100
    }
    ```
  - **Response** (201 Created):
    ```json
    {
      "id": "lead_123",
      "name": "John Doe",
      "job_title": "CEO",
      "company": "Acme Corp",
      "email": "john.doe@acme.com",
      "industry": "Technology",
      "phone_number": "+1-555-0123",
      "headcount": 100,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
    ```
  - **Required Fields**: `name`, `job_title`, `company`, `email`, `industry`
  - **Optional Fields**: `phone_number`, `headcount` (must be between 1 and 1,000,000)

#### Bulk Create Leads

- **POST** `/api/v1/leads/bulk`
  - Creates multiple leads at once (max 10 leads per request)
  - **Request Body**:
    ```json
    {
      "leads": [
        {
          "name": "Jane Smith",
          "job_title": "CTO",
          "company": "Tech Inc",
          "email": "jane@techinc.com",
          "industry": "Technology",
          "headcount": 250
        },
        {
          "name": "Bob Johnson",
          "job_title": "VP Sales",
          "company": "Sales Co",
          "email": "bob@salesco.com",
          "industry": "Marketing",
          "phone_number": "+1-555-0456"
        }
      ]
    }
    ```
  - **Response** (201 Created): Array of `LeadResponse` objects
  - **Limits**: Minimum 1 lead, maximum 10 leads per request

#### List Leads

- **GET** `/api/v1/leads`
  - Lists leads with cursor-based pagination and filtering
  - **Query Parameters**:
    - `cursor` (optional): Cursor for pagination (from `next_cursor` in previous response)
    - `page_size` (optional, default: 20): Number of items per page (1-100)
    - `industry` (optional): Filter by one or more industries (can be repeated: `?industry=Technology&industry=Healthcare`)
    - `min_headcount` (optional): Minimum company headcount (≥ 1)
    - `max_headcount` (optional): Maximum company headcount (≥ 1)
  - **Example Request**: `GET /api/v1/leads?page_size=10&industry=Technology&min_headcount=100`
  - **Response**:
    ```json
    {
      "data": [
        {
          "id": "lead_123",
          "name": "John Doe",
          "job_title": "CEO",
          "company": "Acme Corp",
          "email": "john.doe@acme.com",
          "industry": "Technology",
          "phone_number": "+1-555-0123",
          "headcount": 100,
          "created_at": "2024-01-15T10:30:00Z",
          "updated_at": "2024-01-15T10:30:00Z"
        }
      ],
      "pagination": {
        "total": 150,
        "page_size": 10,
        "next_cursor": "cursor_abc123",
        "prev_cursor": null,
        "has_next": true,
        "has_prev": false
      }
    }
    ```
  - **Pagination**: Uses cursor-based pagination. Use `next_cursor` from the response to fetch the next page.

#### Get Single Lead

- **GET** `/api/v1/leads/{lead_id}`
  - Retrieves detailed information about a specific lead
  - **Path Parameters**:
    - `lead_id`: The unique identifier of the lead
  - **Example Request**: `GET /api/v1/leads/lead_123`
  - **Response**:
    ```json
    {
      "id": "lead_123",
      "name": "John Doe",
      "job_title": "CEO",
      "company": "Acme Corp",
      "email": "john.doe@acme.com",
      "industry": "Technology",
      "phone_number": "+1-555-0123",
      "headcount": 100,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
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

## Key Design Patterns & Best Practices

This API follows several design patterns and best practices to ensure maintainability, testability, and scalability:

### Repository Pattern
- Abstracts data access layer, making it easy to swap in-memory storage with a database later (e.g., PostgreSQL)
- Provides a clean interface for data operations independent of the underlying storage mechanism

### Service Layer
- Business logic is separated from API routes
- Routes handle HTTP concerns, services handle business rules
- Promotes code reusability and easier testing

### Dependency Injection
- Components are loosely coupled and easily testable
- Dependencies are injected through FastAPI's dependency system
- Enables easy mocking and swapping of implementations

### Domain Models
- Separate domain entities from DTOs (Pydantic schemas)
- Domain models represent business entities, schemas handle API contracts
- Clear separation between internal representation and external API

### Cursor-based Pagination
- Scalable pagination for large datasets
- More efficient than offset-based pagination for large result sets
- Better performance with consistent ordering

### Strategy Pattern
- Enrichment service can be swapped with real providers
- Allows for different implementations of the same interface
- Easy to extend with new providers without changing existing code

### Exception Handling
- Custom exceptions with proper HTTP status codes
- Centralized error handling for consistent API responses
- Clear error messages for better developer experience

### Type Safety
- Full type hints throughout the codebase
- Better IDE support with autocomplete and error detection
- Catches errors at development time rather than runtime

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

## Seed Data

The application automatically seeds initial data on startup if the database is empty. This helps with development and testing.

### Automatic Seeding

When the application starts, it checks if there are any leads in the database. If the database is empty, it automatically generates and inserts **100 sample leads**.

### Seed Data Details

The seed data generator creates realistic fake leads using the [Faker](https://faker.readthedocs.io/) library with the following characteristics:

#### Industries
The seed data includes leads from the following industries:
- Technology
- Healthcare
- Finance
- Manufacturing
- Retail
- Education
- Real Estate
- Consulting
- Marketing
- E-commerce

#### Headcount Ranges
Company headcount values are randomly selected from:
- 10, 25, 50, 100, 250, 500, 1,000, 2,500, 5,000, 10,000
- Approximately 20% of leads will have `null` headcount values

#### Generated Fields
Each seed lead includes:
- **name**: Random full name
- **job_title**: Random job title
- **company**: Random company name
- **email**: Company email address
- **industry**: Randomly selected from the industries list above
- **phone_number**: Random phone number (approximately 70% of leads will have a phone number)
- **headcount**: Randomly selected from the headcount ranges (approximately 80% of leads will have a headcount)

### Seed Data Behavior

- **First Startup**: If the database is empty, 100 leads are automatically created
- **Subsequent Starts**: If leads already exist, no seed data is generated
- **Deterministic**: Uses a fixed seed (42) for reproducible results in development

### Manual Seeding

If you need to regenerate seed data, you can:
1. Clear your database
2. Restart the application
3. The seed data will be automatically generated again

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
