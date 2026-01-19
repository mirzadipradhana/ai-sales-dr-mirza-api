from datetime import datetime
from typing import Optional
from uuid import uuid4


class Lead:
    """Lead domain entity - represents business logic."""
    
    def __init__(
        self,
        name: str,
        job_title: str,
        company: str,
        email: str,
        industry: str,
        phone_number: Optional[str] = None,
        headcount: Optional[int] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid4())
        self.name = name
        self.job_title = job_title
        self.company = company
        self.email = email
        self.phone_number = phone_number
        self.industry = industry
        self.headcount = headcount
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "job_title": self.job_title,
            "company": self.company,
            "email": self.email,
            "phone_number": self.phone_number,
            "industry": self.industry,
            "headcount": self.headcount,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
