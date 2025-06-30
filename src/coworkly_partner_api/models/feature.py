"""Feature data model."""

from typing import Dict
from pydantic import BaseModel, ConfigDict


class Feature(BaseModel):
    """Feature model with translations."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    translations: Dict[str, str] 