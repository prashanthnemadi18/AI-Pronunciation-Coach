# AI Pronunciation Coach - API Endpoints

## Overview

This document describes all API endpoints implemented in the FastAPI backend.

## Base URL

- Development: `http://localhost:8000`
- Production: Set via deployment configuration

## Endpoints

### 1. Root Endpoint

**GET /**

Returns API information and available endpoints.

**Response:**
```json
{
  "message": "AI Pronunciation Coach API",
  "version": "1.0.0",
  "endpoints": {
    "evaluate": "/api/pronunciation/evaluate",
    "image": "/api/pronunciation/image",
    "history": "/api/user/{user_id}/history",
    "leaderboard": "/api/leaderboard",
    "health": "/api/health"
  }
}
```

---

### 2. Evaluate Pronunciation

**POST /api/pronunciation/evaluate**

Evaluates pronunciation from audio input through the complete processing pipeline.

**Request Body:**
```json
{
  "audio": "base64_encoded_audio_data",
  "target_word": "hello",
  "user_id": 123,
  "mode": "audio",
  "audio_format": "wav"
}
```

**Parameters:**
- `audio` (string, required): Base64-encoded audio data
- `target_word` (string, required): Word to evaluate pronunciation against
- `user_id` (integer, required): User ID for tracking
- `mode` (string, optional): Mode of interaction - "audio", "image", or "game" (default: "audio")
- `audio_format` (string, optional): Audio format - "wav", "mp3", or "m4a" (default: "wav")

**Response:**
```json
{
  "accuracy_score": 85.5,
  "transcribed_text": "hello",
  "expected_phonemes": ["HH", "AH", "L", "OW"],
  "actual_phonemes": ["HH", "EH", "L", "OW"],
  "phoneme_comparison": {
    "matches": [0, 2, 3],
    "errors": [
      {
        "index": 1,
        "expected": "AH",
        "actual": "EH",
        "type": "substitution"
      }
    ]
  },
  "feedback": {
    "correction_tips": "Try pronouncing the 'e' sound as 'uh' instead of 'eh'.",
    "encouragement": "Great job! You're very close."
  }
}
```

**Processing Pipeline:**
1. Audio Input validation (format, duration)
2. Audio Processing (normalization, noise reduction)
3. Speech Recognition (Whisper transcription)
4. Phoneme Analysis (CMU Dictionary comparison)
5. Scoring (accuracy calculation)
6. Feedback Generation (LLM-powered tips)
7. Database storage

**Error Responses:**
- `400 Bad Request`: Invalid audio format, duration exceeded, no speech detected, word not in dictionary
- `500 Internal Server Error`: Processing failure

**Requirements:** 11.1, 10.2, 12.1

---

### 3. Detect Image Object

**POST /api/pronunciation/image**

Detects the primary object in an uploaded image for Image Mode pronunciation practice.

**Request:**
- Content-Type: `multipart/form-data`
- `image` (file, required): Image file (JPEG, PNG)
- `user_id` (integer, optional): User ID for tracking

**Response:**
```json
{
  "detected_object": "apple",
  "confidence": 0.95,
  "message": "Please pronounce: apple"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid image file
- `500 Internal Server Error`: Detection failure
- `503 Service Unavailable`: Image detection service not configured (missing GEMINI_API_KEY)

**Requirements:** 11.2, 8.2, 8.3

---

### 4. Get User History

**GET /api/user/{user_id}/history**

Retrieves a user's pronunciation attempt history with aggregate statistics.

**Path Parameters:**
- `user_id` (integer, required): User ID

**Query Parameters:**
- `limit` (integer, optional): Maximum number of attempts to return (default: 50)

**Response:**
```json
{
  "user_id": 123,
  "attempts": [
    {
      "id": 1,
      "target_word": "hello",
      "accuracy_score": 85.5,
      "mode": "audio",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_attempts": 50,
  "average_score": 78.3
}
```

**Error Responses:**
- `404 Not Found`: User not found
- `500 Internal Server Error`: Database query failure

**Requirements:** 11.3, 10.4

---

### 5. Get Leaderboard

**GET /api/leaderboard**

Retrieves the game mode leaderboard with top scores.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of entries to return (default: 10)

**Response:**
```json
{
  "leaderboard": [
    {
      "user_id": 123,
      "username": "user1",
      "total_score": 950,
      "words_attempted": 20
    }
  ]
}
```

**Error Responses:**
- `500 Internal Server Error`: Database query failure

**Requirements:** 11.4, 9.5

---

### 6. Health Check

**GET /api/health**

Health check endpoint for monitoring service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "whisper": "healthy",
    "llm": "healthy",
    "image_detection": "unavailable"
  }
}
```

**Service Status Values:**
- `healthy`: Service is operational
- `unhealthy`: Service is not operational
- `unavailable`: Service is not configured

**Overall Status:**
- `healthy`: Critical services (database, whisper) are operational
- `unhealthy`: One or more critical services are down

**Requirements:** 15.5

---

## Error Response Format

All endpoints return errors in a consistent format:

```json
{
  "detail": "Human-readable error message"
}
```

HTTP status codes follow REST conventions:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error
- `503 Service Unavailable`: Service temporarily unavailable

**Requirements:** 11.6, 14.1, 14.2, 14.3, 14.4, 14.5

---

## CORS Configuration

The API is configured with CORS middleware to allow requests from the frontend.

**Allowed Origins:**
- Configured via `CORS_ORIGINS` environment variable
- Default: `http://localhost:5173,http://localhost:3000`

**Allowed Methods:** All (`*`)
**Allowed Headers:** All (`*`)
**Credentials:** Enabled

**Requirements:** 15.4

---

## Running the Server

### Development

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables

Required:
- `LLM_API_KEY` or `GEMINI_API_KEY`: API key for feedback generation
- `GEMINI_API_KEY`: API key for image detection (optional)

Optional:
- `DATABASE_URL`: Database connection string (default: SQLite)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `WHISPER_MODEL_SIZE`: Whisper model size - "tiny", "base", "small" (default: "base")
- `LLM_PROVIDER`: LLM provider - "gemini" or "groq" (default: "gemini")

---

## Testing

Test the API structure:
```bash
cd backend
python test_api_structure.py
```

Test individual endpoints:
```bash
# Health check
curl http://localhost:8000/api/health

# Root endpoint
curl http://localhost:8000/
```

---

## Implementation Notes

### Task 12.1: FastAPI Application with CORS ✓
- FastAPI app initialized with title and description
- CORS middleware configured with environment variable support
- Global exception handling
- Database initialization on startup

### Task 12.2: POST /api/pronunciation/evaluate ✓
- Full processing pipeline orchestration
- Audio validation, processing, transcription
- Phoneme analysis and scoring
- Feedback generation with LLM
- Database storage of attempts
- Comprehensive error handling

### Task 12.3: POST /api/pronunciation/image ✓
- Image upload handling
- Object detection via Gemini Vision API
- Primary object selection
- Error handling for missing API key

### Task 12.4: GET /api/user/{user_id}/history ✓
- User history retrieval with pagination
- Aggregate statistics calculation
- User existence validation

### Task 12.5: GET /api/leaderboard ✓
- Game score retrieval
- Username joining
- Sorted by total score

### Task 12.6: GET /api/health ✓
- Database connection check
- Whisper model availability check
- LLM service availability check
- Image detection service availability check
- Overall status determination

---

## Next Steps

1. Start the FastAPI server
2. Test endpoints with sample data
3. Integrate with frontend application
4. Deploy to production (Render/Railway)
5. Configure environment variables for production
6. Set up monitoring and logging
