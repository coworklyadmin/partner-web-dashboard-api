# Dashboard Metrics API

This document describes the new dashboard metrics API endpoint that securely queries Amplitude's Dashboard REST API on behalf of authenticated partners.

## Overview

The dashboard metrics API provides a secure way to fetch analytics data from Amplitude without exposing credentials to the frontend. It resolves CORS issues and protects Amplitude credentials by proxying requests through the backend.

## Endpoint

### GET /dashboard-metrics

Fetches filtered analytics metrics based on the partner's `partner_space_id` within an optional date range.

#### Authentication

Requires a valid Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

#### Request Parameters

| Parameter    | Type   | Required | Description                     | Example      |
| ------------ | ------ | -------- | ------------------------------- | ------------ |
| `start_date` | string | No       | Start date in YYYY-MM-DD format | `2024-01-01` |
| `end_date`   | string | No       | End date in YYYY-MM-DD format   | `2024-01-31` |

**Note**: If no date parameters are provided, the API defaults to the last 30 days.

#### Request Examples

**Default (last 30 days):**

```
GET /dashboard-metrics/
Authorization: Bearer <firebase-id-token>
```

**Custom date range:**

```
GET /dashboard-metrics/?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer <firebase-id-token>
```

**Start date only (end date defaults to today):**

```
GET /dashboard-metrics/?start_date=2024-01-01
Authorization: Bearer <firebase-id-token>
```

**End date only (start date defaults to 30 days ago):**

```
GET /dashboard-metrics/?end_date=2024-01-31
Authorization: Bearer <firebase-id-token>
```

#### Response

Returns a JSON object with analytics metrics:

```json
{
  "profileViews": 123,
  "favoritesAdded": 45,
  "favoritesRemoved": 12,
  "markerTaps": 87,
  "listViewTaps": 63,
  "reviewsBrowsed": 34,
  "reviewsAdded": 8,
  "externalLinks": 15
}
```

#### Response Fields

| Field              | Description                               | Amplitude Event              |
| ------------------ | ----------------------------------------- | ---------------------------- |
| `profileViews`     | Number of profile navigation events       | `partner_profile_navigation` |
| `favoritesAdded`   | Number of add favorite events             | `add_favorite`               |
| `favoritesRemoved` | Number of remove favorite events          | `remove_favorite`            |
| `markerTaps`       | Number of marker tap events               | `marker_tap`                 |
| `listViewTaps`     | Number of list view item tap events       | `home_listview_item_tap`     |
| `reviewsBrowsed`   | Number of review browse events            | `browse_reviews`             |
| `reviewsAdded`     | Number of review add events               | `add_review`                 |
| `externalLinks`    | Number of external link navigation events | `external_link_navigation`   |

#### Error Responses

| Status Code | Description                                      |
| ----------- | ------------------------------------------------ |
| 400         | Invalid date format or start_date after end_date |
| 401         | Authorization header required or invalid token   |
| 403         | Access denied (not a partner space)              |
| 404         | User profile not found                           |
| 400         | Partner space ID not found in user profile       |
| 500         | Internal server error or Amplitude API error     |

## Configuration

### Environment Variables

The following environment variables must be set:

```bash
# Amplitude API credentials
AMPLITUDE_API_KEY=your_amplitude_api_key
AMPLITUDE_SECRET_KEY=your_amplitude_secret_key

# Optional: Custom Amplitude base URL
AMPLITUDE_BASE_URL=https://amplitude.com/api/2/segmentation
```

### Amplitude Setup

1. **API Credentials**: Obtain your Amplitude project API key and secret from the Amplitude dashboard
2. **Event Properties**: Ensure all target events include the `partner_space_id` custom event property
3. **Event Names**: The API expects the following event names in Amplitude:
   - `partner_profile_navigation`
   - `add_favorite`
   - `remove_favorite`
   - `marker_tap`
   - `home_listview_item_tap`
   - `browse_reviews`
   - `add_review`
   - `external_link_navigation`

## Implementation Details

### Architecture

The implementation consists of two main components:

1. **AmplitudeService** (`src/coworkly_partner_api/services/amplitude_service.py`)

   - Handles authentication with Amplitude API
   - Makes HTTP requests to Amplitude's Dashboard REST API
   - Processes and aggregates event data
   - Maps event names to response field names
   - Supports date range filtering for metrics

2. **Dashboard Metrics API** (`src/coworkly_partner_api/api/dashboard_metrics.py`)

   - Validates Firebase authentication
   - Fetches user profile and extracts space ID
   - Parses and validates date range parameters
   - Calls Amplitude service to get metrics
   - Returns structured JSON response

### Security Features

- **Credential Protection**: Amplitude credentials are stored server-side only
- **Authentication**: Firebase ID token validation ensures only authenticated partners can access data
- **Authorization**: Only users with `type: 'partnerSpace'` can access the endpoint
- **CORS Resolution**: Backend proxy eliminates CORS issues for frontend clients

### Error Handling

- Graceful handling of Amplitude API errors
- Individual event failures don't break the entire response
- Comprehensive error messages for debugging
- Proper HTTP status codes for different error scenarios
- Date format and range validation

## Usage Examples

### Frontend (JavaScript/TypeScript)

```javascript
// Fetch dashboard metrics for last 30 days (default)
const response = await fetch("/dashboard-metrics", {
  headers: {
    Authorization: `Bearer ${firebaseIdToken}`,
    "Content-Type": "application/json",
  },
});

// Fetch dashboard metrics for specific date range
const response = await fetch(
  "/dashboard-metrics?start_date=2024-01-01&end_date=2024-01-31",
  {
    headers: {
      Authorization: `Bearer ${firebaseIdToken}`,
      "Content-Type": "application/json",
    },
  }
);

if (response.ok) {
  const metrics = await response.json();
  console.log("Profile views:", metrics.profileViews);
  console.log("Favorites added:", metrics.favoritesAdded);
  // ... use other metrics
} else {
  console.error("Failed to fetch metrics:", response.statusText);
}
```

### Flutter/Dart

```dart
// Fetch dashboard metrics for specific date range
final response = await http.get(
  Uri.parse('$baseUrl/dashboard-metrics?start_date=2024-01-01&end_date=2024-01-31'),
  headers: {
    'Authorization': 'Bearer $firebaseIdToken',
    'Content-Type': 'application/json',
  },
);

if (response.statusCode == 200) {
  final metrics = jsonDecode(response.body);
  print('Profile views: ${metrics['profileViews']}');
  print('Favorites added: ${metrics['favoritesAdded']}');
  // ... use other metrics
} else {
  print('Failed to fetch metrics: ${response.statusCode}');
}
```

## Testing

Run the test suite to verify the implementation:

```bash
# Run all tests
pytest tests/

# Run dashboard metrics tests specifically
pytest tests/test_dashboard_metrics.py -v
```

## Deployment

1. Set the required environment variables in your deployment environment
2. Deploy the updated code to Firebase Functions
3. Verify the endpoint is accessible and returning expected data
4. Monitor logs for any Amplitude API errors or authentication issues

## Monitoring

Monitor the following for optimal performance:

- Amplitude API response times
- Error rates for individual events
- Authentication failures
- User profile lookup performance
- Overall endpoint response times
- Date range query usage patterns
