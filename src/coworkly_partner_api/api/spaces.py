"""Space-related API routes."""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from firebase_admin import firestore

from ..models.space import Space, SpaceUpdate
from ..services.auth import verify_firebase_token
from ..services.firestore import get_firestore_client, doc_to_dict

router = APIRouter(prefix="/spaces", tags=["spaces"])


@router.get("/{space_id}")
async def get_space(space_id: str, uid: str = Depends(verify_firebase_token)):
    """Fetch a space document from spaces/{spaceId}"""
    try:
        logging.info(f"Space get started: {space_id} by {uid}")

        db = get_firestore_client()
        space_ref = db.collection('spaces').document(space_id)
        space_doc = space_ref.get()
        
        if not space_doc.exists:
            raise HTTPException(status_code=404, detail="Space not found")
        
        # Convert Firestore data to Pydantic model, then dump with aliases
        space_data = doc_to_dict(space_doc)
        space = Space(**space_data)
        return space.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching space: {str(e)}")


@router.patch("/{space_id}")
async def update_space(
    space_id: str, 
    update_data: SpaceUpdate, 
    uid: str = Depends(verify_firebase_token)
):
    """Update fields on spaces/{spaceId}"""
    try:
        logging.info(f"Space update started: {space_id} by {uid}")
        
        # Convert Pydantic model to dict, excluding None values
        update_dict = update_data.model_dump(exclude_none=True, by_alias=True)
        
        if not update_dict:
            logging.warning(f"Space update: no valid fields for {space_id}")
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        db = get_firestore_client()
        space_ref = db.collection('spaces').document(space_id)
        
        # Check if space exists
        space_doc = space_ref.get()
        if not space_doc.exists:
            logging.warning(f"Space update: not found {space_id}")
            raise HTTPException(status_code=404, detail="Space not found")
        
        # Update the document in Firestore
        space_ref.update(update_dict)
        logging.info(f"Space update completed: {space_id}")
        
        # Return updated document using Pydantic model with aliases
        updated_doc = space_ref.get()
        space_data = doc_to_dict(updated_doc)
        space = Space(**space_data)
        
        return space.model_dump()
        
    except HTTPException:
        logging.error(f"HTTPException in space update: {space_id}")
        raise
    except Exception as e:
        logging.error(f"Space update error: {space_id} - {str(e)}")
        logging.error(f"Error type: {type(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error updating space: {str(e)}")