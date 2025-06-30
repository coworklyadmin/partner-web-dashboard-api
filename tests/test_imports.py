#!/usr/bin/env python3
"""
Test script to verify all imports work correctly with Python 3.13
"""

def test_imports():
    """Test all required imports"""
    print("Testing imports for Python 3.13 compatibility...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        assert False, f"FastAPI import failed: {e}"
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        assert False, f"Uvicorn import failed: {e}"
    
    try:
        import firebase_admin
        print(f"✅ Firebase Admin {firebase_admin.__version__}")
    except ImportError as e:
        print(f"❌ Firebase Admin import failed: {e}")
        assert False, f"Firebase Admin import failed: {e}"
    
    try:
        import firebase_functions
        print(f"✅ Firebase Functions {firebase_functions.__version__}")
    except ImportError as e:
        print(f"❌ Firebase Functions import failed: {e}")
        assert False, f"Firebase Functions import failed: {e}"
    
    try:
        import google.cloud.firestore
        print("✅ Google Cloud Firestore")
    except ImportError as e:
        print(f"❌ Google Cloud Firestore import failed: {e}")
        assert False, f"Google Cloud Firestore import failed: {e}"
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        assert False, f"Pydantic import failed: {e}"
    
    try:
        import python_multipart
        print("✅ Python Multipart")
    except ImportError as e:
        print(f"❌ Python Multipart import failed: {e}")
        assert False, f"Python Multipart import failed: {e}"
    
    # Test specific imports from our main module
    try:
        from fastapi import FastAPI, HTTPException, Depends, Header
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel, Field, field_validator
        print("✅ All FastAPI and Pydantic imports")
    except ImportError as e:
        print(f"❌ FastAPI/Pydantic specific imports failed: {e}")
        assert False, f"FastAPI/Pydantic specific imports failed: {e}"
    
    try:
        from firebase_admin import credentials, firestore, auth
        print("✅ All Firebase Admin imports")
    except ImportError as e:
        print(f"❌ Firebase Admin specific imports failed: {e}")
        assert False, f"Firebase Admin specific imports failed: {e}"
    
    # Test our package imports
    try:
        from src.coworkly_partner_api.app import app
        from src.coworkly_partner_api.models import Space, CommunityPost, Feature
        from src.coworkly_partner_api.services import verify_firebase_token, get_firestore_client
        print("✅ All package imports")
    except ImportError as e:
        print(f"❌ Package imports failed: {e}")
        assert False, f"Package imports failed: {e}"
    
    print("\n🎉 All imports successful! The code should work with Python 3.13.")

if __name__ == "__main__":
    test_imports() 