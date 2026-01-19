from typing import Any


class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class LeadNotFoundException(AppException):
    """Lead not found exception."""
    
    def __init__(self, lead_id: str):
        super().__init__(
            message=f"Lead with id '{lead_id}' not found",
            status_code=404,
            details={"lead_id": lead_id}
        )


class ValidationException(AppException):
    """Validation exception."""
    
    def __init__(self, message: str, details: Any = None):
        super().__init__(message=message, status_code=422, details=details)
