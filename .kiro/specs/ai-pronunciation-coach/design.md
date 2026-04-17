# Design Document: AI Pronunciation Coach

## Overview

The AI Pronunciation Coach is a full-stack web application that evaluates pronunciation accuracy through phoneme-level analysis. The system consists of a FastAPI backend with seven core processing modules and a React + TypeScript frontend supporting three interaction modes.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Audio Mode  │  │  Image Mode  │  │  Game Mode   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Core Processing Pipeline                 │   │
│  │  Audio Input → Audio Processing → Speech Recognition │   │
│  │  → Phoneme Analysis → Scoring → Feedback Generation  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Database   │  │ Whisper API  │  │   LLM API    │      │
│  │ (SQLite/PG)  │  │              │  │ (Gemini/Groq)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Backend Design

### Module 1: Audio Input Module

**Purpose:** Capture and validate audio input from users

**Interface:**


```python
class AudioInputModule:
    def accept_recording(audio_data: bytes, format: str) -> AudioData
    def accept_upload(file: UploadFile) -> AudioData
    def validate_audio(audio: AudioData) -> ValidationResult
```

**Implementation Details:**
- Accept audio from microphone recording or file upload
- Validate format (WAV, MP3, M4A)
- Validate duration (max 5 seconds)
- Return AudioData object or validation error
- Provide recording status feedback

**Requirements Coverage:** 1.1, 1.2, 1.3, 1.4, 1.5

### Module 2: Audio Processing Module

**Purpose:** Clean and normalize audio for optimal speech recognition

**Interface:**

```python
class AudioProcessor:
    def normalize_volume(audio: AudioData) -> AudioData
    def remove_noise(audio: AudioData) -> AudioData
    def convert_format(audio: AudioData, target_format: str) -> AudioData
    def process(audio: AudioData) -> ProcessedAudio
```

**Implementation Details:**
- Normalize audio volume using pydub or librosa
- Apply noise reduction filters
- Convert to format compatible with Whisper (typically WAV, 16kHz)
- Complete processing within 2 seconds
- Return descriptive errors on failure

**Requirements Coverage:** 2.1, 2.2, 2.3, 2.4, 2.5

### Module 3: Speech Recognition Module

**Purpose:** Convert speech audio to text transcription

**Interface:**

```python
class SpeechRecognizer:
    def __init__(model_size: str = "base")
    def transcribe(audio: ProcessedAudio) -> TranscriptionResult
    def get_model() -> WhisperModel
```

**Implementation Details:**
- Use OpenAI Whisper API or local Whisper model
- Use small or base model for performance
- Complete transcription within 3 seconds
- Return error if no speech detected
- Pass transcribed text to Phoneme Analyzer

**Requirements Coverage:** 3.1, 3.2, 3.3, 3.4, 3.5

### Module 4: Phoneme Analysis Module

**Purpose:** Extract and compare phoneme sequences

**Interface:**

```python
class PhonemeAnalyzer:
    def __init__(cmu_dict_path: str)
    def get_expected_phonemes(word: str) -> List[str]
    def get_actual_phonemes(transcribed_text: str) -> List[str]
    def compare_phonemes(expected: List[str], actual: List[str]) -> ComparisonResult
    def cache_lookup(word: str) -> Optional[List[str]]
```

**Implementation Details:**
- Load CMU Pronunciation Dictionary
- Convert target word to expected phoneme sequence
- Convert transcribed text to actual phoneme sequence
- Compare sequences and identify matches/differences
- Cache phoneme lookups for performance
- Return error if word not in dictionary

**Data Structures:**

```python
@dataclass
class ComparisonResult:
    expected_phonemes: List[str]
    actual_phonemes: List[str]
    matches: List[Tuple[int, str]]  # (index, phoneme)
    substitutions: List[Tuple[int, str, str]]  # (index, expected, actual)
    missing: List[Tuple[int, str]]  # (index, expected)
    extra: List[Tuple[int, str]]  # (index, actual)
```

**Requirements Coverage:** 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7

### Module 5: Scoring Engine Module

**Purpose:** Calculate pronunciation accuracy scores

**Interface:**

```python
class ScoringEngine:
    def calculate_score(comparison: ComparisonResult) -> ScoringResult
    def weight_matches(matches: List) -> float
    def penalize_errors(substitutions: List, missing: List, extra: List) -> float
```

**Implementation Details:**
- Calculate accuracy score between 0-100
- Weight phoneme matches positively
- Penalize substitutions, missing, and extra phonemes
- Complete scoring within 500ms

**Scoring Algorithm:**

```
score = 100 * (matches / total_expected_phonemes)
score -= (substitutions * 10)
score -= (missing * 15)
score -= (extra * 5)
score = max(0, min(100, score))
```

**Data Structures:**

```python
@dataclass
class ScoringResult:
    accuracy_score: float  # 0-100
    total_phonemes: int
    correct_phonemes: int
    phoneme_details: ComparisonResult
```

**Requirements Coverage:** 5.1, 5.2, 5.3, 5.4, 5.5

### Module 6: Feedback Generation Module

**Purpose:** Generate AI-powered correction tips

**Interface:**

```python
class FeedbackGenerator:
    def __init__(llm_provider: str, api_key: str)
    def generate_feedback(comparison: ComparisonResult, score: float) -> FeedbackResult
    def create_prompt(comparison: ComparisonResult) -> str
    def get_fallback_feedback(comparison: ComparisonResult) -> str
```

**Implementation Details:**
- Use Gemini or Groq API for feedback generation
- Generate specific correction tips for mispronounced phonemes
- Provide encouraging feedback for correct pronunciation
- Complete within 2 seconds
- Return fallback feedback if LLM unavailable

**Prompt Template:**

```
The user attempted to pronounce "{target_word}".
Expected phonemes: {expected}
Actual phonemes: {actual}
Errors: {error_details}

Provide specific, actionable tips to improve pronunciation.
Focus on the incorrect phonemes and how to correct them.
```

**Data Structures:**

```python
@dataclass
class FeedbackResult:
    correction_tips: str
    encouragement: str
    specific_phoneme_guidance: List[Tuple[str, str]]  # (phoneme, tip)
```

**Requirements Coverage:** 6.1, 6.2, 6.3, 6.4, 6.5, 6.6

### Module 7: Image Detection Module

**Purpose:** Detect objects in images for Image Mode

**Interface:**

```python
class ImageDetector:
    def detect_object(image: UploadFile) -> DetectionResult
    def get_primary_object(detections: List) -> str
```

**Implementation Details:**
- Use pre-trained object detection model (e.g., YOLO, ResNet)
- Or use Gemini Vision API for object detection
- Return primary object name as target word
- Handle multiple objects by selecting most prominent

**Data Structures:**

```python
@dataclass
class DetectionResult:
    primary_object: str
    confidence: float
    all_objects: List[Tuple[str, float]]  # (object, confidence)
```

**Requirements Coverage:** 8.2, 8.3

## Database Design

### Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pronunciation attempts table
CREATE TABLE pronunciation_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    target_word VARCHAR(100) NOT NULL,
    transcribed_text VARCHAR(200),
    accuracy_score FLOAT NOT NULL,
    expected_phonemes TEXT,
    actual_phonemes TEXT,
    mode VARCHAR(20) NOT NULL,  -- 'audio', 'image', 'game'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Game scores table
CREATE TABLE game_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_score INTEGER NOT NULL,
    words_attempted INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_attempts_user ON pronunciation_attempts(user_id);
CREATE INDEX idx_attempts_created ON pronunciation_attempts(created_at);
CREATE INDEX idx_scores_user ON game_scores(user_id);
```

**Requirements Coverage:** 10.1, 10.2, 10.3, 10.4, 10.5

## API Design

### Endpoints

#### 1. POST /api/pronunciation/evaluate

**Purpose:** Evaluate pronunciation from audio

**Request:**
```json
{
  "audio": "base64_encoded_audio_data",
  "target_word": "hello",
  "user_id": 123,
  "mode": "audio"
}
```

**Response:**
```json
{
  "accuracy_score": 85.5,
  "transcribed_text": "hello",
  "expected_phonemes": ["HH", "AH", "L", "OW"],
  "actual_phonemes": ["HH", "EH", "L", "OW"],
  "phoneme_comparison": {
    "matches": [0, 2, 3],
    "errors": [{"index": 1, "expected": "AH", "actual": "EH"}]
  },
  "feedback": {
    "correction_tips": "Try pronouncing the 'e' sound as 'uh' instead of 'eh'.",
    "encouragement": "Great job! You're very close."
  }
}
```

**Requirements Coverage:** 11.1

#### 2. POST /api/pronunciation/image

**Purpose:** Evaluate pronunciation from image

**Request:**
```
multipart/form-data:
- image: file
- user_id: 123
```

**Response:**
```json
{
  "detected_object": "apple",
  "confidence": 0.95,
  "message": "Please pronounce: apple"
}
```

Then follows same flow as /evaluate endpoint.

**Requirements Coverage:** 11.2

#### 3. GET /api/user/{user_id}/history

**Purpose:** Retrieve user pronunciation history

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

**Requirements Coverage:** 11.3

#### 4. GET /api/leaderboard

**Purpose:** Retrieve game mode leaderboard

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

**Requirements Coverage:** 11.4

#### 5. GET /api/health

**Purpose:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Requirements Coverage:** 15.5

### Error Responses

All endpoints return errors in this format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {}
}
```

**Requirements Coverage:** 11.6, 14.1, 14.2, 14.3, 14.4, 14.5

## Frontend Design

### Component Architecture

```
App
├── ModeSelector
├── AudioMode
│   ├── AudioRecorder
│   ├── AudioUploader
│   ├── TargetWordInput
│   └── ResultsDisplay
│       ├── ScoreDisplay
│       ├── PhonemeComparison
│       └── FeedbackDisplay
├── ImageMode
│   ├── ImageUploader
│   ├── ObjectDetectionDisplay
│   └── ResultsDisplay (shared)
└── GameMode
    ├── GameTimer
    ├── ScoreTracker
    ├── WordDisplay
    ├── AudioRecorder (shared)
    └── Leaderboard
```

### Key Components

#### ModeSelector Component

**Purpose:** Allow users to choose between Audio, Image, and Game modes

**Interface:**
```typescript
interface ModeSelectorProps {
  onModeChange: (mode: 'audio' | 'image' | 'game') => void;
  currentMode: string;
}
```

**Requirements Coverage:** 13.1

#### AudioRecorder Component

**Purpose:** Record audio from microphone

**Interface:**
```typescript
interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void;
  maxDuration: number;
}
```

**Features:**
- Start/stop recording
- Visual recording indicator
- Duration display
- Audio preview

**Requirements Coverage:** 1.1, 1.5

#### ResultsDisplay Component

**Purpose:** Display pronunciation evaluation results

**Interface:**
```typescript
interface ResultsDisplayProps {
  score: number;
  expectedPhonemes: string[];
  actualPhonemes: string[];
  comparison: PhonemeComparison;
  feedback: Feedback;
}
```

**Features:**
- Score visualization (progress bar or gauge)
- Phoneme-by-phoneme comparison
- Color coding (green for correct, red for incorrect)
- Feedback tips display

**Requirements Coverage:** 7.4, 7.5, 13.2, 13.3

#### ImageUploader Component

**Purpose:** Upload images for Image Mode

**Interface:**
```typescript
interface ImageUploaderProps {
  onImageUpload: (image: File) => void;
}
```

**Requirements Coverage:** 8.1

#### GameMode Component

**Purpose:** Gamified pronunciation practice

**Interface:**
```typescript
interface GameModeProps {
  userId: number;
}
```

**Features:**
- Random word generation
- Countdown timer (30 seconds per word)
- Cumulative score tracking
- Leaderboard display
- Next word button

**Requirements Coverage:** 9.1, 9.2, 9.3, 9.4, 9.5

### State Management

Use React Context or Zustand for global state:

```typescript
interface AppState {
  currentMode: 'audio' | 'image' | 'game';
  userId: number | null;
  currentAttempt: PronunciationAttempt | null;
  isLoading: boolean;
  error: string | null;
}
```

### API Integration

```typescript
class PronunciationAPI {
  static async evaluatePronunciation(
    audio: Blob,
    targetWord: string,
    userId: number,
    mode: string
  ): Promise<EvaluationResult>;
  
  static async detectObject(image: File): Promise<DetectionResult>;
  
  static async getUserHistory(userId: number): Promise<HistoryResult>;
  
  static async getLeaderboard(): Promise<LeaderboardResult>;
}
```

**Requirements Coverage:** 11.1, 11.2, 11.3, 11.4

### Responsive Design

- Mobile-first approach
- Breakpoints: 640px (mobile), 768px (tablet), 1024px (desktop)
- Touch-friendly buttons and controls
- Adaptive layouts for different screen sizes

**Requirements Coverage:** 13.5

### Error Handling

Display user-friendly error messages:

```typescript
const ErrorMessages = {
  INVALID_AUDIO: "Please upload a valid audio file (WAV, MP3, or M4A)",
  AUDIO_TOO_LONG: "Audio must be 5 seconds or less",
  NO_SPEECH: "No speech detected. Please speak more clearly",
  WORD_NOT_FOUND: "This word is not supported yet",
  CONNECTION_ERROR: "Unable to connect to server. Please try again",
  LLM_ERROR: "Feedback generation unavailable. Score still calculated"
};
```

**Requirements Coverage:** 14.1, 14.2, 14.3, 14.4, 14.5

## Deployment Architecture

### Frontend Deployment (Vercel)

**Configuration:**
```json
{
  "framework": "react",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

**Environment Variables:**
- `VITE_API_BASE_URL`: Backend API URL

**Requirements Coverage:** 15.1

### Backend Deployment (Render/Railway)

**Configuration:**
```yaml
# render.yaml
services:
  - type: web
    name: pronunciation-coach-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: WHISPER_API_KEY
        sync: false
      - key: LLM_API_KEY
        sync: false
      - key: CORS_ORIGINS
        value: "https://your-frontend.vercel.app"
```

**Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string
- `WHISPER_API_KEY`: OpenAI Whisper API key
- `LLM_API_KEY`: Gemini or Groq API key
- `CORS_ORIGINS`: Allowed frontend origins
- `CMU_DICT_PATH`: Path to CMU dictionary file

**Requirements Coverage:** 15.2, 15.3, 15.4

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Requirements Coverage:** 15.4

### Health Checks

```python
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": check_database_connection(),
            "whisper": check_whisper_availability(),
            "llm": check_llm_availability()
        }
    }
```

**Requirements Coverage:** 15.5

## Performance Optimization

### Caching Strategy

1. CMU Dictionary phoneme lookups (in-memory cache)
2. Whisper model loading (singleton pattern)
3. LLM responses for common words (Redis cache, optional)

**Requirements Coverage:** 12.2

### Request Timeouts

```python
# FastAPI timeout configuration
@app.post("/api/pronunciation/evaluate")
async def evaluate(request: Request):
    timeout = 6.0  # 6 seconds total
    # Implementation with timeout handling
```

**Requirements Coverage:** 12.4

### Model Selection

- Use Whisper "base" model (balance of speed and accuracy)
- Consider "tiny" model for even faster processing if accuracy acceptable

**Requirements Coverage:** 12.3

### Load Handling

```python
# Rate limiting and load shedding
if current_load > MAX_LOAD:
    raise HTTPException(
        status_code=503,
        detail="Service temporarily unavailable",
        headers={"Retry-After": "60"}
    )
```

**Requirements Coverage:** 12.5

## Technology Stack

### Backend
- Python 3.10+
- FastAPI
- Whisper (OpenAI)
- CMU Pronouncing Dictionary
- Gemini or Groq API
- SQLAlchemy (ORM)
- SQLite (development) / PostgreSQL (production)
- pydub or librosa (audio processing)

### Frontend
- React 18+
- TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)
- React Router (navigation)

### Deployment
- Vercel (frontend)
- Render or Railway (backend)
- PostgreSQL (database)

## Correctness Properties

### Property 1: Audio Duration Validation
**Statement:** For all audio inputs, if duration > 5 seconds, then the system rejects the input.

**Validates:** Requirements 1.3

### Property 2: Score Range Invariant
**Statement:** For all pronunciation evaluations, the accuracy score is always between 0 and 100 inclusive.

**Validates:** Requirements 5.1

### Property 3: Phoneme Comparison Completeness
**Statement:** For all phoneme comparisons, every phoneme in the expected sequence is either matched, substituted, or marked as missing.

**Validates:** Requirements 4.3, 4.4

### Property 4: Processing Time Bounds
**Statement:** For all audio inputs ≤ 5 seconds, the total processing time (audio processing + transcription + analysis + scoring + feedback) is ≤ 6 seconds.

**Validates:** Requirements 2.5, 3.5, 5.5, 6.5, 12.1

### Property 5: Database Consistency
**Statement:** For all pronunciation attempts, if stored in database, then user_id references an existing user.

**Validates:** Requirements 10.2, 10.3

### Property 6: Error Response Format
**Statement:** For all API errors, the response includes an error code, message, and appropriate HTTP status code.

**Validates:** Requirements 11.6, 14.1, 14.2, 14.3, 14.4, 14.5

### Property 7: Phoneme Cache Consistency
**Statement:** For all words in CMU dictionary, if queried twice, the second query returns the same phoneme sequence as the first.

**Validates:** Requirements 4.6

### Property 8: Feedback Generation Fallback
**Statement:** For all pronunciation evaluations, if LLM API fails, the system still returns a score with fallback feedback.

**Validates:** Requirements 6.6, 14.4

## Security Considerations

1. Validate all file uploads (size, format, content)
2. Sanitize user inputs to prevent injection attacks
3. Use environment variables for API keys
4. Implement rate limiting to prevent abuse
5. Use HTTPS for all communications
6. Validate CORS origins

## Future Enhancements

1. Multi-language support
2. Sentence-level pronunciation evaluation
3. Progress tracking and analytics dashboard
4. Social features (share scores, challenges)
5. Offline mode with local Whisper model
6. Custom word lists and lessons
7. Voice comparison (user vs. native speaker)
