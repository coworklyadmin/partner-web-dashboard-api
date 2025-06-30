"""Tests for dashboard metrics API."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from firebase_admin import firestore
from datetime import datetime, timedelta

from src.coworkly_partner_api.app import app
from src.coworkly_partner_api.services.amplitude_service import AmplitudeService


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_verify_firebase_token():
    """Mock Firebase token verification."""
    async def mock_verify_firebase_token(authorization: str = None):
        return "test-user-id"
    return mock_verify_firebase_token


@pytest.fixture
def mock_firestore():
    """Mock Firestore client."""
    with patch('src.coworkly_partner_api.api.dashboard_metrics.get_firestore_client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_amplitude_service():
    """Mock Amplitude service."""
    with patch('src.coworkly_partner_api.api.dashboard_metrics.get_amplitude_service') as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


class TestDashboardMetrics:
    """Test cases for dashboard metrics endpoint."""
    
    def test_get_dashboard_metrics_success(
        self, 
        client, 
        mock_firestore, 
        mock_amplitude_service,
        mock_verify_firebase_token
    ):
        """Test successful dashboard metrics retrieval."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile data
            mock_user_doc = Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {
                'id': 'test-user-id',
                'status': 'active',
                'spaceId': 'test-space-id'
            }
            mock_user_doc.id = 'test-user-id'
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Mock Amplitude metrics response
            mock_amplitude_service.get_dashboard_metrics.return_value = {
                'profileViews': 123,
                'favoritesAdded': 45,
                'favoritesRemoved': 12,
                'markerTaps': 87,
                'listViewTaps': 63,
                'reviewsBrowsed': 34,
                'reviewsAdded': 8,
                'externalLinks': 15
            }
            
            # Make request
            response = client.get(
                "/dashboard-metrics/",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data['profileViews'] == 123
            assert data['favoritesAdded'] == 45
            assert data['favoritesRemoved'] == 12
            assert data['markerTaps'] == 87
            assert data['listViewTaps'] == 63
            assert data['reviewsBrowsed'] == 34
            assert data['reviewsAdded'] == 8
            assert data['externalLinks'] == 15
            
            # Verify calls
            mock_firestore.collection.assert_called_once_with('partner_profiles')
            mock_amplitude_service.get_dashboard_metrics.assert_called_once_with('test-space-id', start_date=None, end_date=None)
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_with_date_range(
        self, 
        client, 
        mock_firestore, 
        mock_amplitude_service,
        mock_verify_firebase_token
    ):
        """Test successful dashboard metrics retrieval with date range."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile data
            mock_user_doc = Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {
                'id': 'test-user-id',
                'status': 'active',
                'spaceId': 'test-space-id'
            }
            mock_user_doc.id = 'test-user-id'
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Mock Amplitude metrics response
            mock_amplitude_service.get_dashboard_metrics.return_value = {
                'profileViews': 50,
                'favoritesAdded': 20,
                'favoritesRemoved': 5,
                'markerTaps': 30,
                'listViewTaps': 25,
                'reviewsBrowsed': 15,
                'reviewsAdded': 3,
                'externalLinks': 8
            }
            
            # Make request with date range
            response = client.get(
                "/dashboard-metrics/?start_date=2024-01-01&end_date=2024-01-31",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data['profileViews'] == 50
            assert data['favoritesAdded'] == 20
            
            # Verify calls with date parameters
            mock_amplitude_service.get_dashboard_metrics.assert_called_once()
            call_args = mock_amplitude_service.get_dashboard_metrics.call_args
            assert call_args[0][0] == 'test-space-id'  # space_id
            assert call_args[1]['start_date'] == datetime(2024, 1, 1)
            assert call_args[1]['end_date'] == datetime(2024, 1, 31)
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_invalid_date_format(
        self, 
        client, 
        mock_firestore,
        mock_verify_firebase_token
    ):
        """Test error when date format is invalid."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile data
            mock_user_doc = Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {
                'id': 'test-user-id',
                'status': 'active',
                'spaceId': 'test-space-id'
            }
            mock_user_doc.id = 'test-user-id'
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Make request with invalid date format
            response = client.get(
                "/dashboard-metrics/?start_date=2024/01/01",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 400
            assert "Invalid start_date format" in response.json()['detail']
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_invalid_date_range(
        self, 
        client, 
        mock_firestore,
        mock_verify_firebase_token
    ):
        """Test error when start_date is after end_date."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile data
            mock_user_doc = Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {
                'id': 'test-user-id',
                'status': 'active',
                'spaceId': 'test-space-id'
            }
            mock_user_doc.id = 'test-user-id'
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Make request with invalid date range
            response = client.get(
                "/dashboard-metrics/?start_date=2024-01-31&end_date=2024-01-01",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 400
            assert "start_date cannot be after end_date" in response.json()['detail']
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_user_profile_not_found(
        self, 
        client, 
        mock_firestore,
        mock_verify_firebase_token
    ):
        """Test error when user profile is not found."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile not found
            mock_user_doc = Mock()
            mock_user_doc.exists = False
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Make request
            response = client.get(
                "/dashboard-metrics/",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 404
            assert response.json()['detail'] == "User profile not found"
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_no_space_id(
        self, 
        client, 
        mock_firestore,
        mock_verify_firebase_token
    ):
        """Test error when user profile has no spaceId."""
        # Override the dependency for this test
        import src.coworkly_partner_api.api.dashboard_metrics as dashboard_metrics_module
        app.dependency_overrides[dashboard_metrics_module.verify_firebase_token] = mock_verify_firebase_token
        
        try:
            # Mock user profile data without spaceId
            mock_user_doc = Mock()
            mock_user_doc.exists = True
            mock_user_doc.to_dict.return_value = {
                'id': 'test-user-id',
                'status': 'active'
                # No spaceId
            }
            mock_user_doc.id = 'test-user-id'
            
            mock_firestore.collection.return_value.document.return_value.get.return_value = mock_user_doc
            
            # Make request
            response = client.get(
                "/dashboard-metrics/",
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Assertions
            assert response.status_code == 400
            assert response.json()['detail'] == "Partner space ID not found in user profile"
        finally:
            app.dependency_overrides = {}
    
    def test_get_dashboard_metrics_no_authorization(self, client):
        """Test error when no authorization header is provided."""
        # Make request without authorization header
        response = client.get("/dashboard-metrics/")
        
        # Assertions
        assert response.status_code == 401
        assert response.json()['detail'] == "Authorization header required"
    
    def test_get_dashboard_metrics_invalid_token(self, client):
        """Test error when Firebase token is invalid."""
        # Make request with invalid token
        response = client.get(
            "/dashboard-metrics/",
            headers={"Authorization": "Bearer invalid-token"}
        )
        
        # Assertions
        assert response.status_code == 401
        assert "Invalid token" in response.json()['detail']


class TestAmplitudeService:
    """Test cases for Amplitude service."""
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    def test_amplitude_service_initialization_no_credentials(self, mock_settings):
        """Test Amplitude service initialization without credentials."""
        mock_settings.AMPLITUDE_API_KEY = ""
        mock_settings.AMPLITUDE_SECRET_KEY = ""
        
        with pytest.raises(ValueError, match="Amplitude API credentials not configured"):
            AmplitudeService()
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    @patch('src.coworkly_partner_api.services.amplitude_service.requests.get')
    def test_get_event_metrics_success(self, mock_get, mock_settings):
        """Test successful event metrics retrieval."""
        # Mock settings
        mock_settings.AMPLITUDE_API_KEY = "test-api-key"
        mock_settings.AMPLITUDE_SECRET_KEY = "test-secret-key"
        mock_settings.AMPLITUDE_BASE_URL = "https://amplitude.com/api/2/segmentation"
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "series": [[10, 15, 20, 25]]  # 4 days of data
            }
        }
        mock_get.return_value = mock_response
        
        # Create service and test
        service = AmplitudeService()
        result = service.get_event_metrics("test-space-id", "test-event")
        
        # Assertions
        assert result == 70  # 10 + 15 + 20 + 25
        mock_get.assert_called_once()
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    @patch('src.coworkly_partner_api.services.amplitude_service.requests.get')
    def test_get_event_metrics_with_date_range(self, mock_get, mock_settings):
        """Test successful event metrics retrieval with date range."""
        # Mock settings
        mock_settings.AMPLITUDE_API_KEY = "test-api-key"
        mock_settings.AMPLITUDE_SECRET_KEY = "test-secret-key"
        mock_settings.AMPLITUDE_BASE_URL = "https://amplitude.com/api/2/segmentation"
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "series": [[5, 10, 15]]  # 3 days of data
            }
        }
        mock_get.return_value = mock_response
        
        # Create service and test with date range
        service = AmplitudeService()
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 3)
        result = service.get_event_metrics("test-space-id", "test-event", start_date, end_date)
        
        # Assertions
        assert result == 30  # 5 + 10 + 15
        mock_get.assert_called_once()
        
        # Verify the API call parameters
        call_args = mock_get.call_args
        params = call_args[1]['params']
        assert params['start'] == '20240101'
        assert params['end'] == '20240103'
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    @patch('src.coworkly_partner_api.services.amplitude_service.requests.get')
    def test_get_dashboard_metrics_with_date_range(self, mock_get, mock_settings):
        """Test successful dashboard metrics retrieval with date range."""
        # Mock settings
        mock_settings.AMPLITUDE_API_KEY = "test-api-key"
        mock_settings.AMPLITUDE_SECRET_KEY = "test-secret-key"
        mock_settings.AMPLITUDE_BASE_URL = "https://amplitude.com/api/2/segmentation"
        
        # Mock API response for multiple events
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "series": [[10, 15]]  # 2 days of data
            }
        }
        mock_get.return_value = mock_response
        
        # Create service and test
        service = AmplitudeService()
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 2)
        result = service.get_dashboard_metrics("test-space-id", start_date, end_date)
        
        # Assertions - should have metrics for all target events
        expected_events = [
            "profileViews", "favoritesAdded", "favoritesRemoved", "markerTaps",
            "listViewTaps", "reviewsBrowsed", "reviewsAdded", "externalLinks"
        ]
        
        for event in expected_events:
            assert event in result
            assert result[event] == 25  # 10 + 15 for each event
        
        # Verify API was called for each event
        assert mock_get.call_count == 8  # One call per event
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    @patch('src.coworkly_partner_api.services.amplitude_service.requests.get')
    def test_get_event_metrics_api_error(self, mock_get, mock_settings):
        """Test handling of Amplitude API errors."""
        # Mock settings
        mock_settings.AMPLITUDE_API_KEY = "test-api-key"
        mock_settings.AMPLITUDE_SECRET_KEY = "test-secret-key"
        mock_settings.AMPLITUDE_BASE_URL = "https://amplitude.com/api/2/segmentation"
        
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        # Create service and test
        service = AmplitudeService()
        
        # The method should return 0 instead of raising an exception
        result = service.get_event_metrics("test-space-id", "test-event")
        assert result == 0
    
    @patch('src.coworkly_partner_api.services.amplitude_service.settings')
    def test_event_to_metric_key_mapping(self, mock_settings):
        """Test event name to metric key mapping."""
        # Mock settings
        mock_settings.AMPLITUDE_API_KEY = "test-api-key"
        mock_settings.AMPLITUDE_SECRET_KEY = "test-secret-key"
        mock_settings.AMPLITUDE_BASE_URL = "https://amplitude.com/api/2/segmentation"
        
        service = AmplitudeService()
        
        # Test mappings
        assert service._event_to_metric_key("partner_profile_navigation") == "profileViews"
        assert service._event_to_metric_key("add_favorite") == "favoritesAdded"
        assert service._event_to_metric_key("remove_favorite") == "favoritesRemoved"
        assert service._event_to_metric_key("marker_tap") == "markerTaps"
        assert service._event_to_metric_key("home_listview_item_tap") == "listViewTaps"
        assert service._event_to_metric_key("browse_reviews") == "reviewsBrowsed"
        assert service._event_to_metric_key("add_review") == "reviewsAdded"
        assert service._event_to_metric_key("external_link_navigation") == "externalLinks"
        assert service._event_to_metric_key("unknown_event") == "unknown_event" 