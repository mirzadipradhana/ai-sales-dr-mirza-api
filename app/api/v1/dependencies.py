from fastapi import Depends
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService


# Singleton instances for in-memory storage
_lead_repository = None


def get_lead_repository() -> LeadRepository:
    """Dependency injection for lead repository."""
    global _lead_repository
    if _lead_repository is None:
        _lead_repository = LeadRepository()
    return _lead_repository


def get_lead_service(
    lead_repository: LeadRepository = Depends(get_lead_repository)
) -> LeadService:
    """Dependency injection for lead service."""
    return LeadService(lead_repository)
