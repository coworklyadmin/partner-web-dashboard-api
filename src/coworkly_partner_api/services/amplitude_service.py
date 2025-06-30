"""Amplitude analytics service."""

import os
import base64
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException

from ..utils.config import settings


class AmplitudeService:
    """Service for interacting with Amplitude Dashboard REST API."""
    
    def __init__(self):
        self.base_url = settings.AMPLITUDE_BASE_URL
        self.api_key = settings.AMPLITUDE_API_KEY
        self.secret_key = settings.AMPLITUDE_SECRET_KEY
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Amplitude API credentials not configured")
        
        # Create Basic Auth header
        credentials = f"{self.api_key}:{self.secret_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.auth_header = f"Basic {encoded_credentials}"
    
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make authenticated request to Amplitude API."""
        try:
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Amplitude API error: {response.text}"
                )
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to Amplitude API: {str(e)}"
            )
    
    def get_event_metrics(
        self, 
        partner_space_id: str, 
        event_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """Get event count for a specific event and partner space."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        # Build event filter as JSON string
        event_filter = {"event_type": event_name}
        
        # Add partner_space_id filter if provided
        if partner_space_id:
            event_filter["user_properties"] = {"partner_space_id": partner_space_id}
        
        params = {
            "e": json.dumps(event_filter),
            "start": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d"),
            "i": "1",  # Daily counts
            "m": "totals"  # Total event counts
        }
        
        try:
            response = self._make_request(params)
            
            # Extract total count from response
            if response.get("data") and response["data"].get("series"):
                # Get the first (and only) series data
                series_data = response["data"]["series"][0]
                if series_data and len(series_data) > 0:
                    # Sum all values in the series
                    total_count = sum(series_data)
                    return total_count
            
            return 0
            
        except Exception as e:
            # Log error but return 0 to avoid breaking the entire dashboard
            print(f"Error fetching {event_name} metrics: {str(e)}")
            return 0
    
    def get_dashboard_metrics(
        self, 
        partner_space_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, int]:
        """Get all dashboard metrics for a partner space within a date range."""
        target_events = [
            "partner_profile_navigation",
            "add_favorite", 
            "remove_favorite",
            "marker_tap",
            "home_listview_item_tap",
            "browse_reviews",
            "add_review",
            "external_link_navigation"
        ]
        
        metrics = {}
        
        for event in target_events:
            # Convert event name to camelCase for response
            metric_key = self._event_to_metric_key(event)
            count = self.get_event_metrics(
                partner_space_id, 
                event, 
                start_date=start_date, 
                end_date=end_date
            )
            metrics[metric_key] = count
        
        return metrics
    
    def _event_to_metric_key(self, event_name: str) -> str:
        """Convert event name to camelCase metric key."""
        event_mapping = {
            "partner_profile_navigation": "profileViews",
            "add_favorite": "favoritesAdded",
            "remove_favorite": "favoritesRemoved", 
            "marker_tap": "markerTaps",
            "home_listview_item_tap": "listViewTaps",
            "browse_reviews": "reviewsBrowsed",
            "add_review": "reviewsAdded",
            "external_link_navigation": "externalLinks"
        }
        
        return event_mapping.get(event_name, event_name)


# Global instance
amplitude_service = None


def get_amplitude_service() -> AmplitudeService:
    """Get Amplitude service instance."""
    global amplitude_service
    if amplitude_service is None:
        amplitude_service = AmplitudeService()
    return amplitude_service 