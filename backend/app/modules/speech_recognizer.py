"""
Speech Recognition Module

Converts speech audio to text transcription using OpenAI Whisper.
Handles transcription with performance optimization and error handling.
"""

from dataclasses import dataclass
from typing import Optional
import time
import threading

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


@dataclass
class TranscriptionResult:
    """Result of speech transcription"""
    success: bool
    transcribed_text: Optional[str] = None
    error_message: Optional[str] = None
    transcription_time: Optional[float] = None
    confidence: Optional[float] = None


class SpeechRecognizer:
    """
    Handles speech-to-text conversion using OpenAI Whisper.
    
    Implements singleton pattern for model loading to optimize performance.
    Uses base or small model for balance of speed and accuracy.
    
    Requirements Coverage: 3.1, 3.2, 3.3, 3.4, 3.5
    """
    
    _instance = None
    _lock = threading.Lock()
    _model = None
    _model_size = None
    
    MAX_TRANSCRIPTION_TIME = 3.0  # seconds
    DEFAULT_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
    
    def __new__(cls, model_size: str = DEFAULT_MODEL_SIZE):
        """
        Implement singleton pattern for model loading.
        
        Requirements: 3.2 (performance optimization)
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, model_size: str = DEFAULT_MODEL_SIZE):
        """
        Initialize the speech recognizer with specified Whisper model.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       Default is 'base' for balance of speed and accuracy
                       
        Requirements: 3.1, 3.2
        """
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "openai-whisper is required for speech recognition. "
                "Install it with: pip install openai-whisper"
            )
        
        # Only load model if not already loaded or if size changed
        if self._model is None or self._model_size != model_size:
            with self._lock:
                if self._model is None or self._model_size != model_size:
                    self._model_size = model_size
                    self._model = whisper.load_model(model_size)
    
    def transcribe(self, audio_data: bytes, audio_format: str = "wav") -> TranscriptionResult:
        """
        Transcribe audio to text using Whisper.
        
        Args:
            audio_data: Processed audio bytes (should be 16kHz WAV)
            audio_format: Audio format (default: 'wav')
            
        Returns:
            TranscriptionResult with transcribed text or error
            
        Requirements: 3.1, 3.3, 3.4, 3.5
        """
        start_time = time.time()
        
        try:
            # Save audio to temporary file for Whisper
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(
                suffix=f".{audio_format}", 
                delete=False
            ) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            try:
                # Transcribe using Whisper
                # Use fp16=False for CPU compatibility
                result = self._model.transcribe(
                    temp_path,
                    fp16=False,
                    language="en",  # Optimize for English
                    task="transcribe"
                )
                
                transcription_time = time.time() - start_time
                
                # Check transcription time constraint (Requirement 3.5)
                if transcription_time > self.MAX_TRANSCRIPTION_TIME:
                    return TranscriptionResult(
                        success=False,
                        error_message=f"Transcription exceeded time limit "
                                     f"({transcription_time:.2f}s > {self.MAX_TRANSCRIPTION_TIME}s)"
                    )
                
                # Extract transcribed text
                transcribed_text = result.get("text", "").strip()
                
                # Check if speech was detected (Requirement 3.3)
                if not transcribed_text:
                    return TranscriptionResult(
                        success=False,
                        error_message="No speech detected in audio. Please speak more clearly.",
                        transcription_time=transcription_time
                    )
                
                # Get confidence if available (segments contain word-level info)
                confidence = None
                if "segments" in result and result["segments"]:
                    # Average confidence across segments
                    confidences = [
                        seg.get("no_speech_prob", 0.0) 
                        for seg in result["segments"]
                    ]
                    if confidences:
                        # Convert no_speech_prob to confidence
                        confidence = 1.0 - (sum(confidences) / len(confidences))
                
                return TranscriptionResult(
                    success=True,
                    transcribed_text=transcribed_text,
                    transcription_time=transcription_time,
                    confidence=confidence
                )
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            transcription_time = time.time() - start_time
            return TranscriptionResult(
                success=False,
                error_message=f"Transcription failed: {str(e)}",
                transcription_time=transcription_time
            )
    
    def get_model(self):
        """
        Get the loaded Whisper model.
        
        Returns:
            Loaded Whisper model instance
            
        Requirements: 3.1
        """
        return self._model
    
    @classmethod
    def reset_instance(cls):
        """
        Reset singleton instance (useful for testing).
        """
        with cls._lock:
            cls._instance = None
            cls._model = None
            cls._model_size = None
