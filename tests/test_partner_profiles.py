"""Tests for partner profiles API."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from firebase_admin import firestore

from src.coworkly_partner_api.app import app
from src.coworkly_partner_api.models.partner_profile import PartnerProfileCreate
from src.coworkly_partner_api.services.auth import get_user_info
from src.coworkly_partner_api.utils.encoding import encrypt_space_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth_dependency():
    app.dependency_overrides[get_user_info] = lambda: {"uid": "test_uid", "email": "test@example.com"}
    yield
    app.dependency_overrides.pop(get_user_info, None)

class TestPartnerProfilesAPI:
    """Test cases for partner profiles API endpoints."""
    
    @patch('src.coworkly_partner_api.services.firestore.get_firestore_client')
    def test_create_partner_profile_success(self, mock_get_firestore):
        """Test successful partner profile creation."""
        # Mock Firestore client
        mock_db = Mock()
        mock_get_firestore.return_value = mock_db
        
        # Mock existing profiles query (no existing profiles)
        mock_profiles_query = Mock()
        mock_db.collection.return_value.where.return_value.stream.return_value = []
        
        # Mock space document (exists)
        mock_space_doc = Mock()
        mock_space_doc.exists = True
        mock_space_doc.to_dict.return_value = {
            'id': 'space123',
            'name': 'Test Space',
            'details': {
                'contact': {
                    'email': 'test@example.com'
                }
            }
        }
        mock_db.collection.return_value.document.return_value.get.return_value = mock_space_doc
        
        # Mock partner profile creation
        mock_new_profile_ref = Mock()
        mock_db.collection.return_value.document.return_value = mock_new_profile_ref
        
        # Mock created profile data
        mock_created_profile = Mock()
        mock_created_profile.to_dict.return_value = {
            'email': 'test@example.com',
            'spaceIds': ['space123'],
            'status': 'active',
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        mock_new_profile_ref.get.return_value = mock_created_profile
        
        # Test data with properly encrypted space ID
        test_data = {
            "hashed_space_id": encrypt_space_id("space123")
        }
        
        # Make request
        response = client.post("/partner-profiles/", json=test_data)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == 'test@example.com'
        assert data['spaceIds'] == ['space123']
        assert data['status'] == 'active'
    
    @patch('src.coworkly_partner_api.services.firestore.get_firestore_client')
    def test_create_partner_profile_already_exists(self, mock_get_firestore):
        """Test partner profile creation when profile already exists."""
        # Mock Firestore client
        mock_db = Mock()
        mock_get_firestore.return_value = mock_db
        
        # Mock existing profiles query (profile exists)
        mock_existing_doc = Mock()
        mock_existing_doc.exists = True
        mock_profiles_query = Mock()
        mock_db.collection.return_value.where.return_value.stream.return_value = [mock_existing_doc]
        
        # Test data with properly encrypted space ID
        test_data = {
            "hashed_space_id": encrypt_space_id("space123")
        }
        
        # Make request
        response = client.post("/partner-profiles/", json=test_data)
        
        # Assertions
        assert response.status_code == 409
        assert "already exists" in response.json()['detail']
    
    @patch('src.coworkly_partner_api.services.firestore.get_firestore_client')
    def test_create_partner_profile_space_not_found(self, mock_get_firestore):
        """Test partner profile creation when space doesn't exist."""
        # Mock Firestore client
        mock_db = Mock()
        mock_get_firestore.return_value = mock_db
        
        # Mock existing profiles query (no existing profiles)
        mock_profiles_query = Mock()
        mock_db.collection.return_value.where.return_value.stream.return_value = []
        
        # Mock space document (doesn't exist)
        mock_space_doc = Mock()
        mock_space_doc.exists = False
        mock_db.collection.return_value.document.return_value.get.return_value = mock_space_doc
        
        # Test data with properly encrypted space ID
        test_data = {
            "hashed_space_id": encrypt_space_id("nonexistent_space")
        }
        
        # Make request
        response = client.post("/partner-profiles/", json=test_data)
        
        # Assertions
        assert response.status_code == 404
        assert "Space not found" in response.json()['detail']
    
    @patch('src.coworkly_partner_api.services.firestore.get_firestore_client')
    def test_create_partner_profile_email_mismatch(self, mock_get_firestore):
        """Test partner profile creation when user email doesn't match space email."""
        # Mock Firestore client
        mock_db = Mock()
        mock_get_firestore.return_value = mock_db
        
        # Mock existing profiles query (no existing profiles)
        mock_profiles_query = Mock()
        mock_db.collection.return_value.where.return_value.stream.return_value = []
        
        # Mock space document (exists but with different email)
        mock_space_doc = Mock()
        mock_space_doc.exists = True
        mock_space_doc.to_dict.return_value = {
            'id': 'space123',
            'name': 'Test Space',
            'details': {
                'contact': {
                    'email': 'different@example.com'  # Different email
                }
            }
        }
        mock_db.collection.return_value.document.return_value.get.return_value = mock_space_doc
        
        # Test data with properly encrypted space ID
        test_data = {
            "hashed_space_id": encrypt_space_id("space123")
        }
        
        # Make request
        response = client.post("/partner-profiles/", json=test_data)
        
        # Assertions
        assert response.status_code == 403
        assert "User email does not match" in response.json()['detail'] 