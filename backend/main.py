# AI Pronunciation Coach - Backend
# FastAPI application entry point

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, UTC
import base64
import os
from sqlalchemy.orm import Session
from sqlalchemy import desc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import database models and connection
import sys
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Configure FFmpeg BEFORE importing any audio modules
from app.modules.ffmpeg_config import configure_ffmpeg
configure_ffmpeg()

from app.models.database import User, PronunciationAttempt, GameScore
from app.models.db_connection import get_db, init_db, check_db_connection

# Import processing modules
from app.modules.audio_input import AudioInputModule, AudioData
from app.modules.audio_processor import AudioProcessor
from app.modules.speech_recognizer import SpeechRecognizer
from app.modules.phoneme_analyzer import PhonemeAnalyzer
from app.modules.scoring_engine import ScoringEngine
from app.modules.feedback_generator import FeedbackGenerator
from app.modules.image_detector import ImageDetector

# Initialize FastAPI app
app = FastAPI(
    title="AI Pronunciation Coach API",
    description="API for pronunciation evaluation with phoneme-level analysis",
    version="1.0.0"
)

# Configure CORS middleware
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and download required resources"""
    init_db()
    
    # Download NLTK data if needed
    try:
        import nltk
        try:
            nltk.data.find('corpora/cmudict')
        except LookupError:
            nltk.download('cmudict', quiet=True)
    except Exception as e:
        print(f"Warning: Could not initialize NLTK data: {e}")

# Initialize processing modules (singletons)
audio_input_module = AudioInputModule()
audio_processor = AudioProcessor()
speech_recognizer = SpeechRecognizer(model_size=os.getenv("WHISPER_MODEL_SIZE", "base"))
phoneme_analyzer = PhonemeAnalyzer()
scoring_engine = ScoringEngine()

# Initialize feedback generator with LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
LLM_API_KEY = os.getenv("LLM_API_KEY", os.getenv("GEMINI_API_KEY", ""))
feedback_generator = FeedbackGenerator(LLM_PROVIDER, LLM_API_KEY) if LLM_API_KEY else None

# Initialize image detector
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
image_detector = ImageDetector(api_provider="gemini", api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# Pydantic models for request/response
class PronunciationEvaluateRequest(BaseModel):
    audio: str  # base64 encoded audio data
    target_word: str
    user_id: int
    mode: str = "audio"  # 'audio', 'image', 'game'
    audio_format: str = "wav"


class PhonemeComparisonResponse(BaseModel):
    matches: List[int]  # indices of matched phonemes
    errors: List[dict]  # list of error details


class FeedbackResponse(BaseModel):
    correction_tips: str
    encouragement: str


class PronunciationEvaluateResponse(BaseModel):
    accuracy_score: float
    transcribed_text: str
    expected_phonemes: List[str]
    actual_phonemes: List[str]
    phoneme_comparison: PhonemeComparisonResponse
    feedback: FeedbackResponse


class ImageDetectionResponse(BaseModel):
    detected_object: str
    confidence: float
    message: str


class PronunciationAttemptResponse(BaseModel):
    id: int
    target_word: str
    accuracy_score: float
    mode: str
    created_at: str


class UserHistoryResponse(BaseModel):
    user_id: int
    attempts: List[PronunciationAttemptResponse]
    total_attempts: int
    average_score: float


class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    total_score: int
    words_attempted: int


class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: dict


# API Endpoints

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
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


@app.post("/api/pronunciation/evaluate", response_model=PronunciationEvaluateResponse)
async def evaluate_pronunciation(
    request: PronunciationEvaluateRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate pronunciation from audio input.
    
    Orchestrates the full processing pipeline:
    1. Audio Input validation
    2. Audio Processing (normalization, noise reduction)
    3. Speech Recognition (Whisper)
    4. Phoneme Analysis (CMU Dictionary)
    5. Scoring (accuracy calculation)
    6. Feedback Generation (LLM)
    7. Database storage
    
    Requirements: 11.1, 10.2, 12.1
    """
    try:
        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(request.audio)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid base64 audio data: {str(e)}"
            )
        
        # Step 1: Validate audio input
        validation_result = audio_input_module.accept_recording(
            audio_bytes,
            request.audio_format
        )
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400,
                detail=validation_result.error_message
            )
        
        audio_data = validation_result.audio_data
        
        # Step 2: Process audio
        processing_result = audio_processor.process(
            audio_data.data,
            audio_data.format,
            audio_data.duration_seconds
        )
        
        if not processing_result.success:
            raise HTTPException(
                status_code=500,
                detail=processing_result.error_message
            )
        
        processed_audio = processing_result.processed_audio
        
        # Step 3: Transcribe speech
        transcription_result = speech_recognizer.transcribe(
            processed_audio.data,
            processed_audio.format
        )
        
        if not transcription_result.success:
            raise HTTPException(
                status_code=400,
                detail=transcription_result.error_message
            )
        
        transcribed_text = transcription_result.transcribed_text
        
        # Step 4: Analyze phonemes
        try:
            expected_phonemes = phoneme_analyzer.get_expected_phonemes(request.target_word)
            actual_phonemes = phoneme_analyzer.get_actual_phonemes(transcribed_text)
            comparison = phoneme_analyzer.compare_phonemes(expected_phonemes, actual_phonemes)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        # Step 5: Calculate score
        scoring_result = scoring_engine.calculate_score(comparison)
        
        # Step 6: Generate feedback
        if feedback_generator:
            try:
                feedback_result = feedback_generator.generate_feedback(
                    comparison,
                    scoring_result.accuracy_score,
                    request.target_word
                )
            except Exception as e:
                # Use fallback feedback if LLM fails
                print(f"Feedback generation error: {e}")
                feedback_result = feedback_generator._get_fallback_feedback(
                    comparison,
                    scoring_result.accuracy_score
                )
        else:
            # No feedback generator available, use simple feedback
            feedback_result = type('obj', (object,), {
                'correction_tips': 'Feedback generation unavailable. Focus on matching expected phonemes.',
                'encouragement': 'Keep practicing!',
                'specific_phoneme_guidance': []
            })()
        
        # Step 7: Store in database
        try:
            # Ensure user exists
            user = db.query(User).filter(User.id == request.user_id).first()
            if not user:
                # Create user if doesn't exist
                user = User(id=request.user_id, username=f"user_{request.user_id}")
                db.add(user)
                db.commit()
            
            # Store pronunciation attempt
            attempt = PronunciationAttempt(
                user_id=request.user_id,
                target_word=request.target_word,
                transcribed_text=transcribed_text,
                accuracy_score=scoring_result.accuracy_score,
                expected_phonemes=' '.join(expected_phonemes),
                actual_phonemes=' '.join(actual_phonemes),
                mode=request.mode,
                created_at=datetime.now(UTC)
            )
            db.add(attempt)
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            # Continue even if database storage fails
        
        # Build response
        phoneme_comparison = PhonemeComparisonResponse(
            matches=[idx for idx, _ in comparison.matches],
            errors=[
                {
                    "index": idx,
                    "expected": exp,
                    "actual": act,
                    "type": "substitution"
                }
                for idx, exp, act in comparison.substitutions
            ] + [
                {
                    "index": idx,
                    "expected": phoneme,
                    "type": "missing"
                }
                for idx, phoneme in comparison.missing
            ] + [
                {
                    "index": idx,
                    "actual": phoneme,
                    "type": "extra"
                }
                for idx, phoneme in comparison.extra
            ]
        )
        
        feedback = FeedbackResponse(
            correction_tips=feedback_result.correction_tips,
            encouragement=feedback_result.encouragement
        )
        
        return PronunciationEvaluateResponse(
            accuracy_score=scoring_result.accuracy_score,
            transcribed_text=transcribed_text,
            expected_phonemes=expected_phonemes,
            actual_phonemes=actual_phonemes,
            phoneme_comparison=phoneme_comparison,
            feedback=feedback
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/pronunciation/image", response_model=ImageDetectionResponse)
async def detect_image_object(
    image: UploadFile = File(...),
    user_id: Optional[int] = None
):
    """
    Detect object in uploaded image for Image Mode.
    
    Returns the detected object name as the target word for pronunciation.
    
    Requirements: 11.2, 8.2, 8.3
    """
    if not image_detector:
        raise HTTPException(
            status_code=503,
            detail="Image detection service unavailable. GEMINI_API_KEY not configured."
        )
    
    try:
        # Read image data
        image_data = await image.read()
        
        # Detect object
        detection_result = image_detector.detect_object(image_data, image.filename)
        
        return ImageDetectionResponse(
            detected_object=detection_result.primary_object,
            confidence=detection_result.confidence,
            message=f"Please pronounce: {detection_result.primary_object}"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image detection failed: {str(e)}"
        )


@app.get("/api/user/{user_id}/history", response_model=UserHistoryResponse)
async def get_user_history(
    user_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve user's pronunciation history.
    
    Returns recent pronunciation attempts with aggregate statistics.
    
    Requirements: 11.3, 10.4
    """
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {user_id} not found"
            )
        
        # Get pronunciation attempts
        attempts = db.query(PronunciationAttempt)\
            .filter(PronunciationAttempt.user_id == user_id)\
            .order_by(desc(PronunciationAttempt.created_at))\
            .limit(limit)\
            .all()
        
        # Calculate statistics
        total_attempts = db.query(PronunciationAttempt)\
            .filter(PronunciationAttempt.user_id == user_id)\
            .count()
        
        if total_attempts > 0:
            all_attempts = db.query(PronunciationAttempt)\
                .filter(PronunciationAttempt.user_id == user_id)\
                .all()
            average_score = sum(a.accuracy_score for a in all_attempts) / total_attempts
        else:
            average_score = 0.0
        
        # Build response
        attempt_responses = [
            PronunciationAttemptResponse(
                id=attempt.id,
                target_word=attempt.target_word,
                accuracy_score=attempt.accuracy_score,
                mode=attempt.mode,
                created_at=attempt.created_at.isoformat()
            )
            for attempt in attempts
        ]
        
        return UserHistoryResponse(
            user_id=user_id,
            attempts=attempt_responses,
            total_attempts=total_attempts,
            average_score=round(average_score, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve user history: {str(e)}"
        )


@app.get("/api/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve game mode leaderboard.
    
    Returns top scores from game mode with usernames.
    
    Requirements: 11.4, 9.5
    """
    try:
        # Get top game scores
        top_scores = db.query(GameScore)\
            .order_by(desc(GameScore.total_score))\
            .limit(limit)\
            .all()
        
        # Build leaderboard with usernames
        leaderboard_entries = []
        for score in top_scores:
            user = db.query(User).filter(User.id == score.user_id).first()
            username = user.username if user else f"user_{score.user_id}"
            
            leaderboard_entries.append(
                LeaderboardEntry(
                    user_id=score.user_id,
                    username=username,
                    total_score=score.total_score,
                    words_attempted=score.words_attempted
                )
            )
        
        return LeaderboardResponse(
            leaderboard=leaderboard_entries
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve leaderboard: {str(e)}"
        )


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Checks status of database, Whisper model, and LLM API.
    
    Requirements: 15.5
    """
    services = {
        "database": "healthy" if check_db_connection() else "unhealthy",
        "whisper": "healthy" if speech_recognizer.get_model() is not None else "unhealthy",
        "llm": "healthy" if feedback_generator is not None else "unavailable",
        "image_detection": "healthy" if image_detector is not None else "unavailable"
    }
    
    # Overall status is healthy if critical services are up
    overall_status = "healthy" if services["database"] == "healthy" and services["whisper"] == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(UTC).isoformat(),
        services=services
    )
