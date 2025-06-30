"""Space-related data models."""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BusinessHours(BaseModel):
    """Business hours for a specific day."""
    model_config = ConfigDict(populate_by_name=True)
    
    open: str
    close: str


class SpaceContact(BaseModel):
    """Contact information for a space."""
    model_config = ConfigDict(populate_by_name=True)
    
    phone: str = ""
    website: str = ""
    emailAddress: str = Field(default="", alias="email")
    facebook: str = Field(default="", alias="facebook")
    instagram: str = Field(default="", alias="instagram")
    twitter: str = Field(default="", alias="twitter")
    tiktok: str = Field(default="", alias="tiktok")
    linkedIn: str = Field(default="", alias="linkedin")

    @field_validator('facebook', 'instagram', 'twitter', 'tiktok', 'linkedIn', mode='before')
    @classmethod
    def convert_none_to_empty(cls, v):
        """Convert None values to empty strings."""
        return "" if v is None else v


class SpaceBusinessHours(BaseModel):
    """Business hours for all days of the week."""
    model_config = ConfigDict(populate_by_name=True)
    
    monday: BusinessHours
    tuesday: BusinessHours
    wednesday: BusinessHours
    thursday: BusinessHours
    friday: BusinessHours
    saturday: BusinessHours
    sunday: BusinessHours


class SpaceDetails(BaseModel):
    """Detailed information about a space."""
    model_config = ConfigDict(populate_by_name=True)
    
    bio: str = ""
    gallery: List[str] = []
    contact: SpaceContact
    businessHours: SpaceBusinessHours = Field(alias="business_hours")
    amenities: List[str] = Field(default_factory=list)


class Space(BaseModel):
    """Complete space model."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    name: str
    geolocation: Dict[str, Any]
    fullAddress: str = Field(alias="full_address")
    mainPhoto: str = Field(default="", alias="main_photo")
    type: str
    rating: Union[int, float] = 0.0
    status: str = "active"
    thumbnailPhoto: str = Field(default="", alias="thumbnail_photo")
    externalUrl: str = Field(default="", alias="external_url")
    details: SpaceDetails


class SpaceUpdate(BaseModel):
    """Model for updating space fields."""
    model_config = ConfigDict(populate_by_name=True)
    
    name: Optional[str] = None
    geolocation: Optional[Dict[str, Any]] = None
    fullAddress: Optional[str] = Field(None, alias="full_address")
    mainPhoto: Optional[str] = Field(None, alias="main_photo")
    type: Optional[str] = None
    rating: Optional[Union[int, float]] = None
    status: Optional[str] = None
    details: Optional[SpaceDetails] = None 