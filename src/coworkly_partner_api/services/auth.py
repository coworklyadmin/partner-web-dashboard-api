"""Authentication services."""

import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header
from google.cloud.firestore import Client


def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("service-account-key.json")
            firebase_admin.initialize_app(cred)
        except FileNotFoundError:
            firebase_admin.initialize_app()


async def verify_firebase_token(authorization: str = Header(None)):
    """Verify Firebase ID token and check partner space access."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        # Remove 'Bearer ' prefix if present
        token = authorization.replace('Bearer ', '')
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        # Check if user is a partner space
        from .firestore import get_firestore_client
        db = get_firestore_client()
        user_profile_ref = db.collection('partner_profiles').document(uid)
        user_profile = user_profile_ref.get()
        
        if not user_profile.exists:
            raise HTTPException(status_code=403, detail="User profile not found")
        
        user_data = user_profile.to_dict()
        if user_data.get('status') != 'active':
            raise HTTPException(status_code=403, detail="Access denied. Partner space required.")
        
        return uid
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}") 