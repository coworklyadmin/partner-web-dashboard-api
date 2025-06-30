#!/bin/bash

# CoWorkly Partner Dashboard API Deployment Script

echo "🚀 Deploying CoWorkly Partner Dashboard API to Firebase Functions..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI is not installed. Please install it first:"
    echo "npm install -g firebase-tools"
    exit 1
fi

# Check if user is logged in (more reliable check)
if ! firebase projects:list &> /dev/null 2>&1; then
    echo "❌ Not logged in to Firebase. Please run:"
    echo "firebase login"
    exit 1
fi

# Check if firebase.json exists
if [ ! -f "firebase.json" ]; then
    echo "❌ firebase.json not found. Please ensure you're in the correct directory."
    exit 1
fi

# Ensure Python venv exists for Firebase Functions
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment (venv)..."
    python3.11 -m venv venv
fi

# Install dependencies into venv
echo "📦 Installing Python dependencies into venv..."
source venv/bin/activate
pip3 install -r requirements.txt
# Optionally install dev dependencies if needed
# pip3 install -e .[dev]
deactivate

# Deploy to Firebase Functions
echo "🌐 Deploying to Firebase Functions..."
firebase deploy --only functions

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo ""
    echo "🔗 Your API is now available at:"
    echo "https://your-project-id.cloudfunctions.net/coworkly_partner_api"
    echo ""
    echo "📚 API Documentation:"
    echo "https://your-project-id.cloudfunctions.net/coworkly_partner_api/docs"
    echo ""
    echo "🧪 Test the API with:"
    echo "python test_api.py"
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi 