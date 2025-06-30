# 🚀 Dashboard Metrics API Setup Guide

This guide will help you set up the Dashboard Metrics API with Amplitude integration.

## 📋 Prerequisites

- Python 3.10+
- Firebase project with Firestore
- Amplitude project with API access
- Firebase service account key

## 🔧 Step-by-Step Setup

### 1. **Install Dependencies**

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. **Get Amplitude API Credentials**

1. **Log into Amplitude Dashboard**

   - Go to [https://analytics.amplitude.com](https://analytics.amplitude.com)
   - Sign in to your account

2. **Navigate to API Keys**

   - Go to **Settings** → **Projects** → **[Your Project]** → **API Keys**
   - Copy your **API Key** and **Secret Key**

3. **Verify Event Setup**
   - Ensure these events exist in your Amplitude project:
     - `partner_profile_navigation`
     - `add_favorite`
     - `remove_favorite`
     - `marker_tap`
     - `home_listview_item_tap`
     - `browse_reviews`
     - `add_review`
     - `external_link_navigation`
   - Each event should include a `partner_space_id` custom property

### 3. **Configure Environment Variables**

#### **Option A: Interactive Setup (Recommended)**

Run the setup script:

```bash
python setup_amplitude.py
```

This will:

- Prompt you for your Amplitude credentials
- Create a `.env` file automatically
- Set environment variables for the current session

#### **Option B: Manual Setup**

Create a `.env` file in your project root:

```bash
# Amplitude API Configuration
AMPLITUDE_API_KEY=your_amplitude_api_key_here
AMPLITUDE_SECRET_KEY=your_amplitude_secret_key_here

# Optional: Custom Amplitude base URL
AMPLITUDE_BASE_URL=https://analytics.amplitude.com/api/2/events/segmentation

# Firebase Configuration
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=true
```

#### **Option C: System Environment Variables**

```bash
# macOS/Linux
export AMPLITUDE_API_KEY="your_amplitude_api_key_here"
export AMPLITUDE_SECRET_KEY="your_amplitude_secret_key_here"

# Windows (Command Prompt)
set AMPLITUDE_API_KEY=your_amplitude_api_key_here
set AMPLITUDE_SECRET_KEY=your_amplitude_secret_key_here

# Windows (PowerShell)
$env:AMPLITUDE_API_KEY="your_amplitude_api_key_here"
$env:AMPLITUDE_SECRET_KEY="your_amplitude_secret_key_here"
```

### 4. **Firebase Configuration**

1. **Service Account Key**

   - Download your Firebase service account key from Firebase Console
   - Place it as `service-account-key.json` in your project root
   - Update `FIREBASE_PROJECT_ID` in your `.env` file

2. **Firestore Collections**
   - Ensure you have a `partner_profiles` collection
   - Each partner profile should have:
     - `type: "partnerSpace"`
     - `spaceId: "your_space_id"`

### 5. **Test the Setup**

#### **Run Tests**

```bash
# Run all tests
pytest tests/

# Run dashboard metrics tests specifically
pytest tests/test_dashboard_metrics.py -v
```

#### **Test API Endpoint**

1. **Start the API server**:

```bash
# Development server
uvicorn src.coworkly_partner_api.app:app --reload --host 0.0.0.0 --port 8080

# Or using the main.py
python main.py
```

2. **Test the endpoint**:

```bash
# Using curl (replace with your Firebase ID token)
curl -X GET "http://localhost:8080/dashboard-metrics/" \
  -H "Authorization: Bearer YOUR_FIREBASE_ID_TOKEN" \
  -H "Content-Type: application/json"
```

3. **Using the example script**:

```bash
# Update the Firebase token in examples/dashboard_metrics_example.py
python examples/dashboard_metrics_example.py
```

### 6. **Verify Configuration**

Run the verification script:

```bash
python setup_amplitude.py
```

This will check if your credentials are properly configured.

## 🔍 Troubleshooting

### **Common Issues**

#### **1. "Amplitude API credentials not configured"**

**Solution**: Set the environment variables:

```bash
export AMPLITUDE_API_KEY="your_key"
export AMPLITUDE_SECRET_KEY="your_secret"
```

#### **2. "User profile not found"**

**Solution**: Ensure the user exists in `partner_profiles` collection with:

- `type: "partnerSpace"`
- `spaceId: "your_space_id"`

#### **3. "Partner space ID not found in user profile"**

**Solution**: Add `spaceId` field to the user's partner profile document.

#### **4. "Amplitude API error"**

**Solution**:

- Verify your API credentials are correct
- Check that the events exist in Amplitude
- Ensure `partner_space_id` property is set on events

#### **5. Import Errors**

**Solution**: Install missing dependencies:

```bash
pip install -r requirements.txt
```

### **Debug Mode**

Enable debug mode in your `.env` file:

```bash
DEBUG=true
```

This will provide more detailed error messages.

## 🚀 Deployment

### **Firebase Functions**

1. **Set Environment Variables in Firebase**:

```bash
firebase functions:config:set amplitude.api_key="your_key"
firebase functions:config:set amplitude.secret_key="your_secret"
```

2. **Deploy**:

```bash
firebase deploy --only functions
```

### **Other Platforms**

Set the environment variables in your deployment platform:

- **Heroku**: Use the dashboard or CLI
- **AWS Lambda**: Use environment variables in function configuration
- **Google Cloud Run**: Use environment variables in service configuration

## 📊 Monitoring

After deployment, monitor:

1. **API Response Times**
2. **Error Rates**
3. **Authentication Failures**
4. **Amplitude API Errors**

## 🎯 Next Steps

1. **Integrate with Frontend**: Use the API endpoint in your Flutter Web app
2. **Add Caching**: Consider caching metrics to improve performance
3. **Add More Metrics**: Extend the API with additional analytics
4. **Set Up Monitoring**: Configure alerts for API errors

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the test logs: `pytest tests/test_dashboard_metrics.py -v`
3. Check the API documentation: `docs/dashboard-metrics-api.md`
4. Verify your Amplitude event setup

---

**🎉 You're all set!** Your Dashboard Metrics API is now ready to use.
