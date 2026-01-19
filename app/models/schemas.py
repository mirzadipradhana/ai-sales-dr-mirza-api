from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LeadBase(BaseModel):
    """Base lead schema."""
    name: str = Field(..., min_length=1, max_length=200)
    job_title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    industry: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=50)
    headcount: Optional[int] = Field(None, ge=1, le=1_000_000)


class LeadCreate(LeadBase):
    """Schema for creating a lead."""
    pass


class LeadBulkCreate(BaseModel):
    """Schema for bulk creating leads."""
    leads: list[LeadCreate] = Field(..., min_length=1, max_length=10)


class LeadResponse(LeadBase):
    """Schema for lead response."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Schema for paginated lead list response."""
    data: list[LeadResponse]
    pagination: "PaginationMetadata"


class PaginationMetadata(BaseModel):
    """Pagination metadata."""
    total: int
    page_size: int
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None
    has_next: bool
    has_prev: bool
