from datetime import datetime
from typing import Optional
from app.models.domain import Lead
from app.repositories.base import BaseRepository
from app.utils.pagination import CursorPage, decode_cursor


class LeadRepository(BaseRepository[Lead]):
    """In-memory lead repository."""
    
    def __init__(self):
        self._storage: dict[str, Lead] = {}
    
    async def create(self, lead: Lead) -> Lead:
        """Create a new lead."""
        self._storage[lead.id] = lead
        return lead
    
    async def bulk_create(self, leads: list[Lead]) -> list[Lead]:
        """Bulk create leads."""
        for lead in leads:
            self._storage[lead.id] = lead
        return leads
    
    async def get_by_id(self, lead_id: str) -> Optional[Lead]:
        """Get lead by ID."""
        return self._storage.get(lead_id)
    
    async def update(self, lead: Lead) -> Lead:
        """Update a lead."""
        lead.updated_at = datetime.utcnow()
        self._storage[lead.id] = lead
        return lead
    
    async def delete(self, lead_id: str) -> bool:
        """Delete a lead."""
        if lead_id in self._storage:
            del self._storage[lead_id]
            return True
        return False
    
    async def find_all_paginated(
        self,
        page_size: int = 20,
        cursor: Optional[str] = None,
        industry: Optional[list[str]] = None,
        min_headcount: Optional[int] = None,
        max_headcount: Optional[int] = None,
    ) -> CursorPage[Lead]:
        """Find all leads with cursor-based pagination and filters."""
        
        # Apply filters
        filtered_leads = list(self._storage.values())
        
        if industry:
            filtered_leads = [
                lead for lead in filtered_leads 
                if lead.industry in industry
            ]
        
        if min_headcount is not None:
            filtered_leads = [
                lead for lead in filtered_leads 
                if lead.headcount is not None and lead.headcount >= min_headcount
            ]
        
        if max_headcount is not None:
            filtered_leads = [
                lead for lead in filtered_leads 
                if lead.headcount is not None and lead.headcount <= max_headcount
            ]
        
        # Sort by created_at DESC, then by id for deterministic ordering
        filtered_leads.sort(key=lambda x: (x.created_at, x.id), reverse=True)
        
        total = len(filtered_leads)
        
        # Handle cursor-based pagination
        start_index = 0
        if cursor:
            cursor_data = decode_cursor(cursor)
            cursor_created_at = cursor_data.get("created_at")
            cursor_id = cursor_data.get("id")
            
            if cursor_created_at and cursor_id:
                # Find the position after the cursor
                for idx, lead in enumerate(filtered_leads):
                    if (lead.created_at.isoformat() == cursor_created_at and 
                        lead.id == cursor_id):
                        start_index = idx + 1
                        break
        
        # Slice data
        end_index = start_index + page_size
        page_data = filtered_leads[start_index:end_index]
        
        # Generate next/prev cursors
        next_cursor = None
        prev_cursor = None
        has_next = end_index < total
        has_prev = start_index > 0
        
        if has_next and page_data:
            last_item = page_data[-1]
            next_cursor = self._create_cursor(last_item)
        
        if has_prev and start_index > 0:
            # For prev, we'd need to implement reverse pagination logic
            # Simplified: just indicate there's previous data
            pass
        
        return CursorPage(
            data=page_data,
            total=total,
            page_size=page_size,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
            has_next=has_next,
            has_prev=has_prev,
        )
    
    def _create_cursor(self, lead: Lead) -> str:
        """Create cursor from lead."""
        from app.utils.pagination import create_cursor
        return create_cursor(lead.created_at.isoformat(), lead.id)
    
    def count(self) -> int:
        """Count total leads."""
        return len(self._storage)
