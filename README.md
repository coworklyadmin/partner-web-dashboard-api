# CoWorkly Partner Dashboard API

A Python REST API built with FastAPI and deployed as a single Firebase Function for the CoWorkly Partner Dashboard.

## Features

- 🔐 Firebase Authentication with ID token verification
- 🏢 Partner space access control
- 📍 Space management (GET/PATCH operations)
- 📝 Community post creation
- 🎯 Features collection querying
- 🌐 CORS enabled for web clients
- 📊 Pydantic data validation

## Endpoints

### Authentication

All endpoints require a valid Firebase ID token in the `Authorization` header:

```
Authorization: Bearer <firebase_id_token>
```

### 1. GET /spaces/{spaceId}

Fetch a space document from `spaces/{spaceId}`

**Response:** Full space details including nested fields

### 2. PATCH /spaces/{spaceId}

Update fields on `spaces/{spaceId}`

**Body:** JSON object with fields to update
**Response:** Updated space document

### 3. POST /posts

Create a new community post

**Body:** JSON matching the `CommunityPost` model
**Response:** Created post with server-generated timestamp

### 4. GET /features

Query all documents from the `features` collection group

**Response:** Array of feature objects with translations

## Data Models

### CommunityPost

```python
{
    "id": "string",
    "author": {"id": "string", "name": "string"},
    "content": "string",
    "createdAt": "datetime",
    "imageUrls": ["string"],
    "externalLinks": ["string"],
    "likesCount": 0,
    "commentsCount": 0,
    "isLikedByUser": false
}
```

### Space

```python
{
    "id": "string",
    "name": "string",
    "geolocation": {"lat": float, "lng": float},
    "fullAddress": "string",
    "mainPhoto": "string",
    "type": "string",
    "rating": 0.0,
    "status": "string",
    "thumbnailPhoto": "string",
    "externalUrl": "string",
    "details": SpaceDetails
}
```

## Setup

### Prerequisites

- Python 3.11+
- Firebase CLI
- Firebase project with Firestore enabled

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Firebase credentials:**

   - Download your Firebase service account key
   - Save it as `service-account-key.json` in the project root

3. **Run locally:**

   ```bash
   python main.py
   ```

4. **Test endpoints:**

   ```bash
   # Health check
   curl http://localhost:8080/health

   # Get space (requires auth token)
   curl -H "Authorization: Bearer <token>" http://localhost:8080/spaces/space123
   ```

### Deployment

1. **Install Firebase CLI:**

   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase:**

   ```bash
   firebase login
   ```

3. **Initialize Firebase project (if not already done):**

   ```bash
   firebase init functions
   ```

4. **Deploy the function:**
   ```bash
   firebase deploy --only functions
   ```

## Security

- All endpoints verify Firebase ID tokens
- Input validation and sanitization on all endpoints
- CORS configured for web client access

## Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:

- `401`: Invalid or missing authentication
- `403`: Access denied (not a partner space)
- `404`: Resource not found
- `400`: Bad request (validation errors)
- `500`: Internal server error

## Development Notes

- The API uses FastAPI for routing and validation
- Firebase Admin SDK for authentication and Firestore access
- Pydantic models for data validation
- CORS middleware enabled for cross-origin requests
- Server-side timestamps for post creation

## Testing

Test the deployed function:

```bash
# Replace with your actual function URL
curl -H "Authorization: Bearer <token>" \
     https://your-project.cloudfunctions.net/coworkly_partner_api/spaces/space123
```

## Environment Variables

For production deployment, ensure these are configured in Firebase:

- `GOOGLE_APPLICATION_CREDENTIALS` (automatically handled by Firebase Functions)
- Firestore security rules configured appropriately
