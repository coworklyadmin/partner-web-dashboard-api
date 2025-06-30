#!/usr/bin/env python3
"""
Setup script for Amplitude API credentials.

This script helps you configure the required environment variables
for the Dashboard Metrics API.

Usage:
    python setup_amplitude.py
"""

import os
import getpass
from pathlib import Path


def setup_amplitude_credentials():
    """Interactive setup for Amplitude API credentials."""
    print("🔧 Amplitude API Setup")
    print("=" * 50)
    
    # Get Amplitude API Key
    print("\n1. Amplitude API Key")
    print("   - Go to your Amplitude project dashboard")
    print("   - Navigate to Settings > Projects > [Your Project] > API Keys")
    print("   - Copy your API Key")
    
    api_key = getpass.getpass("   Enter your Amplitude API Key: ").strip()
    
    if not api_key:
        print("   ❌ API Key is required!")
        return False
    
    # Get Amplitude Secret Key
    print("\n2. Amplitude Secret Key")
    print("   - In the same API Keys section")
    print("   - Copy your Secret Key")
    
    secret_key = getpass.getpass("   Enter your Amplitude Secret Key: ").strip()
    
    if not secret_key:
        print("   ❌ Secret Key is required!")
        return False
    
    # Optional: Custom base URL
    print("\n3. Amplitude Base URL (Optional)")
    print("   - Default: https://analytics.amplitude.com/api/2/events/segmentation")
    
    base_url = input("   Enter custom base URL (or press Enter for default): ").strip()
    if not base_url:
        base_url = "https://analytics.amplitude.com/api/2/events/segmentation"
    
    # Create .env file
    env_content = f"""# Amplitude API Configuration
AMPLITUDE_API_KEY={api_key}
AMPLITUDE_SECRET_KEY={secret_key}
AMPLITUDE_BASE_URL={base_url}

# Firebase Configuration (update these as needed)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=true
"""
    
    # Write to .env file
    env_file = Path(".env")
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"\n✅ Created {env_file}")
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return False
    
    # Set environment variables for current session
    os.environ["AMPLITUDE_API_KEY"] = api_key
    os.environ["AMPLITUDE_SECRET_KEY"] = secret_key
    os.environ["AMPLITUDE_BASE_URL"] = base_url
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Your Amplitude credentials are now configured.")
    print("\nNext steps:")
    print("1. Update FIREBASE_PROJECT_ID in .env file")
    print("2. Ensure service-account-key.json is in place")
    print("3. Run: python -m pytest tests/test_dashboard_metrics.py")
    print("4. Start your API server")
    
    return True


def verify_credentials():
    """Verify that Amplitude credentials are properly configured."""
    print("\n🔍 Verifying Configuration")
    print("=" * 30)
    
    api_key = os.getenv("AMPLITUDE_API_KEY")
    secret_key = os.getenv("AMPLITUDE_SECRET_KEY")
    base_url = os.getenv("AMPLITUDE_BASE_URL")
    
    if not api_key:
        print("❌ AMPLITUDE_API_KEY not set")
        return False
    
    if not secret_key:
        print("❌ AMPLITUDE_SECRET_KEY not set")
        return False
    
    print(f"✅ AMPLITUDE_API_KEY: {api_key[:8]}...")
    print(f"✅ AMPLITUDE_SECRET_KEY: {secret_key[:8]}...")
    print(f"✅ AMPLITUDE_BASE_URL: {base_url}")
    
    return True


def main():
    """Main setup function."""
    print("🚀 Dashboard Metrics API - Amplitude Setup")
    print("=" * 60)
    
    # Check if credentials already exist
    if verify_credentials():
        print("\n✅ Amplitude credentials are already configured!")
        response = input("Do you want to reconfigure? (y/N): ").strip().lower()
        if response != 'y':
            return
    
    # Run setup
    if setup_amplitude_credentials():
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please try again.")


if __name__ == "__main__":
    main() 