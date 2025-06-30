"""Dashboard metrics data model."""

from pydantic import BaseModel, ConfigDict


class DashboardMetrics(BaseModel):
    """Dashboard metrics model matching Amplitude response."""
    model_config = ConfigDict(populate_by_name=True)
    
    profileViews: int = 0
    favoritesAdded: int = 0
    favoritesRemoved: int = 0
    markerTaps: int = 0
    listViewTaps: int = 0
    reviewsBrowsed: int = 0
    reviewsAdded: int = 0
    externalLinks: int = 0 