# CoWorkly Partner Dashboard API Documentation

## Overview

The CoWorkly Partner Dashboard API provides endpoints for managing coworking spaces, community posts, features, and analytics. All endpoints return data in camelCase format for consistency.

**Base URL**: `https://your-firebase-function-url.com` (Production)  
**Local Development**: `http://localhost:8080`

## Authentication

All API endpoints require Firebase Authentication. Include the Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase_id_token>
```

### Authentication Requirements

- User must have a valid Firebase ID token

### Error Responses

- `401 Unauthorized`: Missing or invalid authorization header
- `403 Forbidden`: User is not a partner space

## API Endpoints

### Health Check

#### GET /health

Health check endpoint to verify API status.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

### Spaces

#### GET /spaces/{space_id}

Fetch a specific space by ID.

**Parameters:**

- `space_id` (string, required): The unique identifier of the space

**Response:**

```json
{
  "id": "space_123",
  "name": "CoWork Hub Downtown",
  "geolocation": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "fullAddress": "123 Main St, San Francisco, CA 94105",
  "mainPhoto": "https://example.com/photo.jpg",
  "type": "coworking",
  "rating": 4.5,
  "status": "active",
  "thumbnailPhoto": "https://example.com/thumbnail.jpg",
  "externalUrl": "https://coworkhub.com",
  "details": {
    "bio": "A modern coworking space in the heart of downtown",
    "gallery": [
      "https://example.com/gallery1.jpg",
      "https://example.com/gallery2.jpg"
    ],
    "contact": {
      "phone": "+1-555-0123",
      "website": "https://coworkhub.com",
      "emailAddress": "hello@coworkhub.com",
      "facebook": "https://facebook.com/coworkhub",
      "instagram": "https://instagram.com/coworkhub",
      "twitter": "https://twitter.com/coworkhub",
      "tiktok": "https://tiktok.com/@coworkhub",
      "linkedIn": "https://linkedin.com/company/coworkhub"
    },
    "businessHours": {
      "monday": { "open": "09:00", "close": "18:00" },
      "tuesday": { "open": "09:00", "close": "18:00" },
      "wednesday": { "open": "09:00", "close": "18:00" },
      "thursday": { "open": "09:00", "close": "18:00" },
      "friday": { "open": "09:00", "close": "18:00" },
      "saturday": { "open": "10:00", "close": "16:00" },
      "sunday": { "open": "10:00", "close": "16:00" }
    },
    "ammenities": ["WiFi", "Coffee", "Meeting Rooms", "Printing"]
  }
}
```

**Error Responses:**

- `404 Not Found`: Space not found
- `500 Internal Server Error`: Server error

#### PATCH /spaces/{space_id}

Update specific fields of a space.

**Parameters:**

- `space_id` (string, required): The unique identifier of the space

**Request Body:**

```json
{
  "name": "Updated Space Name",
  "rating": 4.8,
  "status": "active",
  "details": {
    "bio": "Updated bio description"
  }
}
```

**Allowed Fields for Update:**

- `name`: Space name
- `geolocation`: Location coordinates
- `fullAddress`: Full address string
- `mainPhoto`: Main photo URL
- `type`: Space type
- `rating`: Space rating (float)
- `status`: Space status
- `thumbnailPhoto`: Thumbnail photo URL
- `externalUrl`: External website URL
- `details`: Space details object

**Response:** Returns the updated space document in the same format as GET

**Error Responses:**

- `400 Bad Request`: No valid fields to update
- `404 Not Found`: Space not found
- `500 Internal Server Error`: Server error

---

### Posts

#### POST /posts

Create a new community post.

**Request Body:**

```json
{
  "author": {
    "id": "user_123",
    "name": "John Doe"
  },
  "content": "Welcome to our new coworking space! We're excited to have you here.",
  "spaceId": "space_123",
  "imageUrls": [
    "https://example.com/post-image1.jpg",
    "https://example.com/post-image2.jpg"
  ],
  "externalLinks": ["https://example.com/event-link"],
  "likesCount": 0,
  "commentsCount": 0,
  "isLikedByUser": false
}
```

**Required Fields:**

- `author`: Object with `id` and `name` fields
- `content`: Post content (non-empty string)

**Optional Fields:**

- `spaceId`: ID of the space this post belongs to
- `imageUrls`: Array of image URLs
- `externalLinks`: Array of external link URLs
- `likesCount`: Number of likes (default: 0)
- `commentsCount`: Number of comments (default: 0)
- `isLikedByUser`: Whether the current user liked the post (default: false)

**Response:**

```json
{
  "id": "post_456",
  "author": {
    "id": "user_123",
    "name": "John Doe"
  },
  "content": "Welcome to our new coworking space! We're excited to have you here.",
  "spaceId": "space_123",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "imageUrls": [
    "https://example.com/post-image1.jpg",
    "https://example.com/post-image2.jpg"
  ],
  "externalLinks": ["https://example.com/event-link"],
  "likesCount": 0,
  "commentsCount": 0,
  "isLikedByUser": false
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields or invalid data
- `500 Internal Server Error`: Server error

#### GET /posts/{post_id}

Fetch a specific post by ID.

**Parameters:**

- `post_id` (string, required): The unique identifier of the post

**Response:**

```json
{
  "id": "post_456",
  "author": {
    "id": "user_123",
    "name": "John Doe"
  },
  "content": "Welcome to our new coworking space! We're excited to have you here.",
  "spaceId": "space_123",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "imageUrls": [
    "https://example.com/post-image1.jpg",
    "https://example.com/post-image2.jpg"
  ],
  "externalLinks": ["https://example.com/event-link"],
  "likesCount": 5,
  "commentsCount": 2,
  "isLikedByUser": true
}
```

**Error Responses:**

- `404 Not Found`: Post not found
- `500 Internal Server Error`: Server error

#### PATCH /posts/{post_id}

Update specific fields of a post.

**Parameters:**

- `post_id` (string, required): The unique identifier of the post

**Request Body:**

```json
{
  "content": "Updated post content",
  "likesCount": 5,
  "isLikedByUser": true
}
```

**Allowed Fields for Update:**

- `content`: Post content (cannot be empty)
- `imageUrls`: Array of image URLs
- `externalLinks`: Array of external link URLs
- `likesCount`: Number of likes
- `commentsCount`: Number of comments
- `isLikedByUser`: Whether the current user liked the post

**Response:** Returns the updated post in the same format as GET

**Error Responses:**

- `400 Bad Request`: No valid fields to update or invalid content
- `404 Not Found`: Post not found
- `500 Internal Server Error`: Server error

#### DELETE /posts/{post_id}

Delete a post by ID.

**Parameters:**

- `post_id` (string, required): The unique identifier of the post

**Response:**

```json
{
  "message": "Post deleted successfully"
}
```

**Error Responses:**

- `404 Not Found`: Post not found
- `500 Internal Server Error`: Server error

#### GET /posts/space/{space_id}

Fetch all posts for a specific space.

**Parameters:**

- `space_id` (string, required): The unique identifier of the space

**Response:** Returns an array of posts in the same format as GET /posts/{post_id}

**Error Responses:**

- `500 Internal Server Error`: Server error

---

### Partner Profiles

#### POST /partner-profiles/

Create a new partner profile for a space. Only the user whose Firebase Auth email matches the space's contact email can create a profile for that space.

**Authentication:**

- Requires a valid Firebase ID token in the `Authorization` header.

**Request Body:**

```json
{
  "hashedSpaceId": "<Fernet-encrypted-space-id>"
}
```

- `hashed_space_id`: The Fernet-encrypted space ID, as provided in the registration link parameter `a`.

**How it works:**

- The backend decrypts the space ID.
- The backend fetches the user's email from the Firebase Auth token.
- The backend fetches the space document and checks the contact email.
- The backend only creates the partner profile if the emails match.

**Response:**

```json
{
  "id": "<profile_id>",
  "email": "user@example.com",
  "spaceIds": ["space123"],
  "status": "active",
  "createdAt": "2024-06-15T12:00:00Z",
  "updatedAt": "2024-06-15T12:00:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid or missing encrypted space ID
- `403 Forbidden`: User email does not match the space's contact email
- `404 Not Found`: Space not found
- `409 Conflict`: Partner profile already exists for this space
- `500 Internal Server Error`: Server error

---

### Features

#### GET /features

Fetch features by type.

**Query Parameters:**

- `feature_type` (string, required): Type of features to retrieve. Must be either "workspace_features" or "coliving_features"

**Response:**

```json
[
  {
    "id": "feature_1",
    "translations": {
      "en": "High-Speed WiFi",
      "es": "WiFi de Alta Velocidad",
      "fr": "WiFi Haute Vitesse"
    }
  },
  {
    "id": "feature_2",
    "translations": {
      "en": "Meeting Rooms",
      "es": "Salas de Reuniones",
      "fr": "Salles de Réunion"
    }
  }
]
```

**Error Responses:**

- `500 Internal Server Error`: Server error

---

### Dashboard Metrics

#### GET /dashboard-metrics

Fetch dashboard analytics metrics for the authenticated partner.

**Query Parameters:**

- `start_date` (string, optional): Start date in YYYY-MM-DD format
- `end_date` (string, optional): End date in YYYY-MM-DD format

**Response:**

```json
{
  "profileViews": 1250,
  "favoritesAdded": 890,
  "favoritesRemoved": 45,
  "markerTaps": 3200,
  "listViewTaps": 2100,
  "reviewsBrowsed": 1800,
  "reviewsAdded": 150,
  "externalLinks": 320
}
```

**Error Responses:**

- `400 Bad Request`: Invalid date format or date range
- `404 Not Found`: User profile not found
- `500 Internal Server Error`: Server error

---

## Data Models

### Space Model

```typescript
interface Space {
  id: string;
  name: string;
  geolocation: {
    latitude: number;
    longitude: number;
  };
  fullAddress: string;
  mainPhoto: string;
  type: string;
  rating: number;
  status: string;
  thumbnailPhoto: string;
  externalUrl: string;
  details: SpaceDetails;
}

interface SpaceDetails {
  bio: string;
  gallery: string[];
  contact: SpaceContact;
  businessHours: SpaceBusinessHours;
  ammenities: string[];
}

interface SpaceContact {
  phone: string;
  website: string;
  emailAddress: string;
  facebook: string;
  instagram: string;
  twitter: string;
  tiktok: string;
  linkedIn: string;
}

interface SpaceBusinessHours {
  monday: BusinessHours;
  tuesday: BusinessHours;
  wednesday: BusinessHours;
  thursday: BusinessHours;
  friday: BusinessHours;
  saturday: BusinessHours;
  sunday: BusinessHours;
}

interface BusinessHours {
  open: string; // Format: "HH:MM"
  close: string; // Format: "HH:MM"
}
```

### Community Post Model

```typescript
interface CommunityPost {
  id?: string;
  author: {
    id: string;
    name: string;
  };
  content: string;
  spaceId?: string;
  createdAt?: string; // ISO 8601 timestamp
  imageUrls: string[];
  externalLinks: string[];
  likesCount: number;
  commentsCount: number;
  isLikedByUser: boolean;
}
```

### Feature Model

```typescript
interface Feature {
  id: string;
  translations: {
    [languageCode: string]: string;
  };
}
```

### Dashboard Metrics Model

```typescript
interface DashboardMetrics {
  profileViews: number;
  favoritesAdded: number;
  favoritesRemoved: number;
  markerTaps: number;
  listViewTaps: number;
  reviewsBrowsed: number;
  reviewsAdded: number;
  externalLinks: number;
}
```

### Health Response Model

```typescript
interface HealthResponse {
  status: string;
  timestamp: string; // ISO 8601 timestamp
}
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## CORS Configuration

The API supports CORS with the following configuration:

- **Allowed Origins**: All origins (configurable)
- **Allowed Methods**: GET, POST, PATCH, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization
- **Credentials**: Supported

---

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Default Limit**: 100 requests per minute per IP
- **Authentication Endpoints**: 10 requests per minute per IP
- **File Upload Endpoints**: 20 requests per minute per IP

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

---

## Versioning

The API uses URL versioning. Current version: v1

All endpoints are prefixed with `/api/v1/` (e.g., `/api/v1/spaces`)

---

## Development Setup

### Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
