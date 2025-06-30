"""Health check data model."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response model."""
    model_config = ConfigDict(populate_by_name=True)
    
    status: str
    timestamp: datetime 