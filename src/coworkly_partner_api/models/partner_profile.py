"""Partner profile data model."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class PartnerProfile(BaseModel):
    """Partner profile model."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = None
    email: str
    spaceIds: List[str] = Field(alias="space_ids")
    status: str = "active"
    createdAt: Optional[datetime] = Field(None, alias="created_at")
    updatedAt: Optional[datetime] = Field(None, alias="updated_at")


class PartnerProfileCreate(BaseModel):
    """Model for creating a partner profile."""
    model_config = ConfigDict(populate_by_name=True)
    
    hashedSpaceId: str = Field(alias="hashed_space_id", description="Fernet encrypted space ID from URL parameter 'a'") 