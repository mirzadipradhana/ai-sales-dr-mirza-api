from typing import Optional
from app.core.exception import LeadNotFoundException
from app.models.domain import Lead
from app.models.schemas import LeadCreate
from app.repositories.lead_repository import LeadRepository
from app.utils.pagination import CursorPage


class LeadService:
    """Lead service - encapsulates business logic."""
    
    def __init__(
        self, 
        lead_repository: LeadRepository,
    ):
        self.lead_repo = lead_repository
    
    async def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead."""
        lead = Lead(
            name=lead_data.name,
            job_title=lead_data.job_title,
            company=lead_data.company,
            email=lead_data.email,
            phone_number=lead_data.phone_number,
            industry=lead_data.industry,
            headcount=lead_data.headcount,
        )
        return await self.lead_repo.create(lead)
    
    async def bulk_create_leads(self, leads_data: list[LeadCreate]) -> list[Lead]:
        """Bulk create leads."""
        leads = [
            Lead(
                name=lead_data.name,
                job_title=lead_data.job_title,
                company=lead_data.company,
                email=lead_data.email,
                phone_number=lead_data.phone_number,
                industry=lead_data.industry,
                headcount=lead_data.headcount,
            )
            for lead_data in leads_data
        ]
        return await self.lead_repo.bulk_create(leads)
    
    async def get_lead(self, lead_id: str) -> Lead:
        """Get a lead by ID."""
        lead = await self.lead_repo.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException(lead_id)
        return lead
    
    async def list_leads(
        self,
        page_size: int = 20,
        cursor: Optional[str] = None,
        industry: Optional[list[str]] = None,
        min_headcount: Optional[int] = None,
        max_headcount: Optional[int] = None,
    ) -> CursorPage[Lead]:
        """List leads with pagination and filters."""
        return await self.lead_repo.find_all_paginated(
            page_size=page_size,
            cursor=cursor,
            industry=industry,
            min_headcount=min_headcount,
            max_headcount=max_headcount,
        )