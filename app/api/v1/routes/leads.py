from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from app.api.v1.dependencies import get_lead_service
from app.core.config import Settings, get_settings
from app.models.schemas import (
    LeadBulkCreate,
    LeadCreate,
    LeadListResponse,
    LeadResponse,
    PaginationMetadata,
)
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lead",
)
async def create_lead(
    lead_data: LeadCreate,
    lead_service: LeadService = Depends(get_lead_service),
):
    """Create a new lead in the system."""
    lead = await lead_service.create_lead(lead_data)
    return LeadResponse(**lead.to_dict())


@router.post(
    "/bulk",
    response_model=list[LeadResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Bulk create leads",
)
async def bulk_create_leads(
    bulk_data: LeadBulkCreate,
    lead_service: LeadService = Depends(get_lead_service),
):
    """Create multiple leads at once (max 1000)."""
    leads = await lead_service.bulk_create_leads(bulk_data.leads)
    return [LeadResponse(**lead.to_dict()) for lead in leads]


@router.get(
    "",
    response_model=LeadListResponse,
    summary="List leads with pagination and filters",
)
async def list_leads(
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    industry: Optional[list[str]] = Query(None, description="Filter by industries"),
    min_headcount: Optional[int] = Query(None, ge=1, description="Minimum headcount"),
    max_headcount: Optional[int] = Query(None, ge=1, description="Maximum headcount"),
    lead_service: LeadService = Depends(get_lead_service),
    settings: Settings = Depends(get_settings),
):
    """
    List leads with cursor-based pagination and filtering.
    
    **Filters:**
    - industry: Filter by one or more industries
    - min_headcount: Minimum company headcount
    - max_headcount: Maximum company headcount
    
    **Pagination:**
    - Uses cursor-based pagination for efficient scaling
    - Use `next_cursor` from response for next page
    """
    page_size = min(page_size, settings.MAX_PAGE_SIZE)
    
    result = await lead_service.list_leads(
        page_size=page_size,
        cursor=cursor,
        industry=industry,
        min_headcount=min_headcount,
        max_headcount=max_headcount,
    )
    
    return LeadListResponse(
        data=[LeadResponse(**lead.to_dict()) for lead in result.data],
        pagination=PaginationMetadata(
            total=result.total,
            page_size=result.page_size,
            next_cursor=result.next_cursor,
            prev_cursor=result.prev_cursor,
            has_next=result.has_next,
            has_prev=result.has_prev,
        ),
    )


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Get a single lead",
)
async def get_lead(
    lead_id: str,
    lead_service: LeadService = Depends(get_lead_service),
):
    """Get detailed information about a specific lead."""
    lead = await lead_service.get_lead(lead_id)
    return LeadResponse(**lead.to_dict())

