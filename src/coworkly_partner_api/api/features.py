"""Feature-related API routes."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Literal

from ..services.auth import verify_firebase_token
from ..services.firestore import get_firestore_client, doc_to_dict
from ..models.feature import Feature

router = APIRouter(prefix="/features", tags=["features"])


@router.get("/", response_model=List[Feature])
async def get_features(
    feature_type: Literal["workspace_features", "coliving_features"] = Query(
        ..., 
        description="Type of features to retrieve: 'workspace_features' or 'coliving_features'"
    ),
    uid: str = Depends(verify_firebase_token)
):
    """Query features from the specified collection"""
    try:
        # Query documents from the specific features collection
        db = get_firestore_client()
        
        # Get all subtype documents within the feature_type collection
        subtype_docs = db.collection(feature_type).stream()
        
        features = []
        for subtype_doc in subtype_docs:
            # For each subtype, get all features from its features subcollection
            features_query = subtype_doc.reference.collection('features')
            features_docs = features_query.stream()
            
            for doc in features_docs:
                feature_data = doc_to_dict(doc)
                # Create Feature object with proper structure
                feature = Feature(
                    id=doc.id,
                    translations={
                        'en': feature_data.get('en', ''),
                        'es': feature_data.get('es', ''),
                        'fr': feature_data.get('fr', '')
                    }
                )
                features.append(feature)
        
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching features: {str(e)}") 