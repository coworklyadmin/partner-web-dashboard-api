"""Dashboard metrics API routes."""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query

from ..models.dashboard_metrics import DashboardMetrics
from ..services.auth import verify_firebase_token
from ..services.firestore import get_firestore_client, doc_to_dict
from ..services.amplitude_service import get_amplitude_service

router = APIRouter(prefix="/dashboard-metrics", tags=["dashboard-metrics"])


@router.get("/")
async def get_dashboard_metrics(
    uid: str = Depends(verify_firebase_token),
    space_ids: Optional[List[str]] = Query(None, description="Comma-separated list of space IDs to query"),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    """Fetch dashboard analytics metrics for the authenticated partner within a date range."""
    try:
        # Parse date parameters if provided
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid start_date format. Use YYYY-MM-DD"
                )
        
        if end_date:
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid end_date format. Use YYYY-MM-DD"
                )
        
        # Validate date range if both dates are provided
        if parsed_start_date and parsed_end_date and parsed_start_date > parsed_end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be after end_date"
            )
        
        # Handle space_ids parameter
        if space_ids is None:
            # Fallback to getting space IDs from user profile
            db = get_firestore_client()
            user_profile_ref = db.collection('partner_profiles').document(uid)
            user_profile = user_profile_ref.get()
            
            if not user_profile.exists:
                raise HTTPException(status_code=404, detail="User profile not found")
            
            user_data = doc_to_dict(user_profile)
            user_space_ids = user_data.get('spaceIds', [])  # Now expecting array of strings
            
            if not user_space_ids:
                raise HTTPException(
                    status_code=400, 
                    detail="Partner space IDs not found in user profile"
                )
            
            # If it's a single string, convert to list
            if isinstance(user_space_ids, str):
                user_space_ids = [user_space_ids]
            
            space_ids = user_space_ids
        else:
            # Validate that space_ids is a list
            if not isinstance(space_ids, list) or len(space_ids) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="space_ids must be a non-empty list"
                )
        
        # Get Amplitude service and fetch metrics
        amplitude_service = get_amplitude_service()
        metrics_data = amplitude_service.get_dashboard_metrics(
            space_ids, 
            start_date=parsed_start_date, 
            end_date=parsed_end_date
        )
        
        # Convert to Pydantic model for consistent response
        metrics_model = DashboardMetrics(**metrics_data)
        return metrics_model.model_dump()
        
    except HTTPException:
        raise
    except ValueError as e:
        # Amplitude credentials not configured
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching dashboard metrics: {str(e)}"
        ) 