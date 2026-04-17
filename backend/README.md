# AI Pronunciation Coach - Backend

FastAPI-based backend for pronunciation evaluation and feedback generation.

## Setup

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Environment Variables

- `DATABASE_URL`: Database connection string (SQLite for dev, PostgreSQL for prod)
- `LLM_PROVIDER`: LLM provider (gemini or groq)
- `GEMINI_API_KEY`: Google Gemini API key
- `GROQ_API_KEY`: Groq API key
- `ALLOWED_ORIGINS`: CORS allowed origins (comma-separated)
- `WHISPER_MODEL_SIZE`: Whisper model size (tiny, base, small, medium, large)

## Running the Server

### Quick Start

Using the startup script (recommended):
```bash
python start_server.py --dev  # Development mode with auto-reload
python start_server.py        # Production mode
```

### Manual Start

Development mode:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Documentation

Once the server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Endpoints Documentation: See `API_ENDPOINTS.md`

## API Endpoints

For detailed API documentation, see [API_ENDPOINTS.md](./API_ENDPOINTS.md)

### Summary

#### Core Endpoints
- `POST /api/pronunciation/evaluate` - Evaluate pronunciation from audio
  - Accepts base64-encoded audio and target word
  - Returns accuracy score, phoneme comparison, and AI-powered feedback
  - Stores attempt in database

- `POST /api/pronunciation/image` - Detect object in image for Image Mode
  - Accepts image file upload
  - Returns detected object name as target word
  - Uses Gemini Vision API

- `GET /api/user/{user_id}/history` - Get user's pronunciation history
  - Returns paginated list of attempts
  - Includes aggregate statistics (total attempts, average score)

- `GET /api/leaderboard` - Get game mode leaderboard
  - Returns top scores sorted by total score
  - Includes usernames and words attempted

- `GET /api/health` - Health check endpoint
  - Returns status of all services (database, Whisper, LLM, image detection)
  - Used for monitoring and deployment health checks

#### Request/Response Examples

**Evaluate Pronunciation:**
```bash
curl -X POST http://localhost:8000/api/pronunciation/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "audio": "base64_encoded_audio_data",
    "target_word": "hello",
    "user_id": 1,
    "mode": "audio",
    "audio_format": "wav"
  }'
```

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoint handlers
│   ├── models/       # SQLAlchemy database models
│   └── modules/      # Core processing modules
│       ├── audio_input.py
│       ├── audio_processor.py
│       ├── speech_recognizer.py
│       ├── phoneme_analyzer.py
│       ├── scoring_engine.py
│       ├── feedback_generator.py
│       └── image_detector.py
├── main.py           # FastAPI application entry point
└── requirements.txt  # Python dependencies
```

## Core Modules

- **Audio Input Module**: Handles audio recording and file uploads
- **Audio Processor**: Normalizes and cleans audio data
- **Speech Recognizer**: Converts speech to text using Whisper
- **Phoneme Analyzer**: Compares phoneme sequences using CMU Dictionary
- **Scoring Engine**: Calculates pronunciation accuracy scores
- **Feedback Generator**: Generates AI-powered correction tips
- **Image Detector**: Detects objects in images for vocabulary practice

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## Deployment

### Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Railway

1. Create a new project
2. Connect your repository
3. Add environment variables
4. Railway will auto-detect and deploy

## License

MIT
