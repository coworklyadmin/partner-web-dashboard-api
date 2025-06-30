"""Community post data model."""

from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CommunityPost(BaseModel):
    """Community post model."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = None
    author: Dict[str, str] = Field(..., description="Must contain id and name")
    content: str
    spaceId: Optional[str] = Field(None, alias="space_id")
    createdAt: Optional[datetime] = Field(None, alias="created_at")
    imageUrls: List[str] = Field(default_factory=list, alias="image_urls")
    externalLinks: List[str] = Field(default_factory=list, alias="external_links")
    likesCount: int = Field(default=0, alias="likes_count")
    commentsCount: int = Field(default=0, alias="comments_count")
    isLikedByUser: bool = Field(default=False, alias="is_liked_by_user")

    @field_validator('author')
    @classmethod
    def validate_author(cls, v):
        """Validate that author contains required fields."""
        if not isinstance(v, dict):
            raise ValueError('author must be a dictionary')
        if 'id' not in v or 'name' not in v:
            raise ValueError('author must contain id and name fields')
        return v


class PostUpdate(BaseModel):
    """Model for updating post fields."""
    model_config = ConfigDict(populate_by_name=True)
    
    content: Optional[str] = None
    imageUrls: Optional[List[str]] = Field(None, alias="image_urls")
    externalLinks: Optional[List[str]] = Field(None, alias="external_links")
    likesCount: Optional[int] = Field(None, alias="likes_count")
    commentsCount: Optional[int] = Field(None, alias="comments_count")
    isLikedByUser: Optional[bool] = Field(None, alias="is_liked_by_user")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate that content is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError('Content cannot be empty')
        return v 