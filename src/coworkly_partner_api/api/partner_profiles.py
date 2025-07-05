"""Partner profile API routes."""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from firebase_admin import firestore

from ..models.partner_profile import PartnerProfile, PartnerProfileCreate
from ..services.auth import get_user_info
from ..services.firestore import get_firestore_client, doc_to_dict
from ..utils.encoding import decrypt_space_id, decrypt_email

router = APIRouter(prefix="/partner-profiles", tags=["partner-profiles"])

@router.post("/")
async def create_partner_profile(
    profile_data: PartnerProfileCreate, 
    user_info: dict = Depends(get_user_info)
):
    """Create a new partner profile"""
    try:
        db = get_firestore_client()
        uid = user_info['uid']
        user_email = user_info['email']
        
        # Decrypt the encrypted space ID
        decoded_space_id = decrypt_space_id(profile_data.hashedSpaceId)
        if not decoded_space_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid encrypted space ID format"
            )
        
        # Check if there's already a partner profile with the decoded space id
        # Query partner_profiles collection for the decoded space id
        profiles_query = db.collection('partner_profiles').where('spaceIds', 'array_contains', decoded_space_id)
        existing_profiles = profiles_query.stream()
        
        # Check if any profile exists with this space ID
        for doc in existing_profiles:
            if doc.exists:
                raise HTTPException(
                    status_code=409, 
                    detail="Partner profile already exists with this space ID"
                )
        
        # Query spaces collection to get space info
        space_ref = db.collection('spaces').document(decoded_space_id)
        space_doc = space_ref.get()
        
        if not space_doc.exists:
            raise HTTPException(
                status_code=404, 
                detail="Space not found with the provided space ID"
            )
        
        # Get space data to verify email
        space_data = doc_to_dict(space_doc)
        space_contact = space_data.get('details', {}).get('contact', {})
        space_email = space_contact.get('email', '')
        
        # Verify that the user's email matches the space's email
        if user_email.lower() != space_email.lower():
            raise HTTPException(
                status_code=403,
                detail="User email does not match the space's contact email"
            )
        
        # Prepare partner profile data
        profile_dict = {
            'email': user_email,  # Use the verified email from Firebase Auth
            'spaceIds': [decoded_space_id],
            'status': 'active',
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        # Add to Firestore using the UID as document ID
        partner_profiles_ref = db.collection('partner_profiles')
        new_profile_ref = partner_profiles_ref.document(uid)
        new_profile_ref.set(profile_dict)
        
        # Get the created document and convert to Pydantic model
        created_profile = new_profile_ref.get()
        profile_data_dict = doc_to_dict(created_profile)
        profile_model = PartnerProfile(**profile_data_dict)
        
        return profile_model.model_dump()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating partner profile: {str(e)}"
        ) 