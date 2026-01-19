import base64
import json
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class CursorPage(BaseModel, Generic[T]):
    """Generic cursor-based pagination result."""
    model_config = {"arbitrary_types_allowed": True}
    
    data: list[T]
    total: int
    page_size: int
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None
    has_next: bool = False
    has_prev: bool = False


def encode_cursor(data: dict) -> str:
    """Encode cursor data to base64 string."""
    json_str = json.dumps(data, sort_keys=True)
    return base64.urlsafe_b64encode(json_str.encode()).decode()


def decode_cursor(cursor: str) -> dict:
    """Decode base64 cursor string to dict."""
    try:
        json_str = base64.urlsafe_b64decode(cursor.encode()).decode()
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def create_cursor(last_item_created_at: str, last_item_id: str) -> str:
    """Create cursor from last item timestamp and id."""
    return encode_cursor({
        "created_at": last_item_created_at,
        "id": last_item_id
    })
