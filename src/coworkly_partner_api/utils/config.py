"""Configuration utilities."""

import os
from typing import List
from pathlib import Path

# Load .env file if it exists
env_file = Path(".env")
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # If python-dotenv is not installed, manually load the file
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value


class Settings:
    """Application settings."""
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_KEY_PATH", 
        "coworkly-17cfa-firebase-adminsdk-fbsvc-56d5b70778.json"
    )
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8080"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:52308",
        "https://your-frontend-domain.com",
        "*"  # Allow all origins for development
    ]
    
    # Security
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1"
    ]
    
    # Firestore Collections
    COLLECTIONS = {
        "spaces": "spaces",
        "posts": "posts",
        "partner_profiles": "partner_profiles",
        "features": "features"
    }
    
    # Amplitude Configuration
    AMPLITUDE_API_KEY: str = os.getenv("AMPLITUDE_API_KEY", "")
    AMPLITUDE_SECRET_KEY: str = os.getenv("AMPLITUDE_SECRET_KEY", "")
    AMPLITUDE_BASE_URL: str = os.getenv(
        "AMPLITUDE_BASE_URL",
        "https://amplitude.com/api/2/segmentation"
    )
    
    # Encryption Configuration
    FERNET_KEY: str = os.getenv("FERNET_KEY", "")


settings = Settings() 