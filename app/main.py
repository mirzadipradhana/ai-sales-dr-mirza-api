from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import leads
from app.core.config import get_settings
from app.api.v1.dependencies import get_lead_repository
from app.utils.seed_data import SeedDataGenerator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - seed data on startup."""
    settings = get_settings()
    
    # Seed initial data
    lead_repo = get_lead_repository()
    if lead_repo.count() == 0:
        generator = SeedDataGenerator()
        seed_leads = generator.generate_leads(count=100)
        await lead_repo.bulk_create(seed_leads)
        print(f"✅ Seeded {len(seed_leads)} leads")
    
    yield
    
    # Cleanup (if needed)
    print("🔌 Shutting down...")


# Initialize settings
settings = get_settings()

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
    }


app.include_router(leads.router, prefix=settings.API_V1_PREFIX)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


# For Vercel deployment
handler = app
