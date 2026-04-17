"""
Audio Input Module

Handles audio input capture and validation for the pronunciation coach system.
Supports both microphone recording and file uploads with format and duration validation.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from io import BytesIO
import os

try:
    from pydub import AudioSegment
    from pydub.exceptions import CouldntDecodeError
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


@dataclass
class AudioData:
    """Represents validated audio data"""
    data: bytes
    format: str
    duration_seconds: float
    sample_rate: int = 16000


@dataclass
class ValidationResult:
    """Result of audio validation"""
    is_valid: bool
    error_message: Optional[str] = None
    audio_data: Optional[AudioData] = None


class AudioInputModule:
    """
    Handles audio input capture and validation.
    
    Validates:
    - Audio format (WAV, MP3, M4A)
    - Audio duration (max 5 seconds)
    
    Requirements Coverage: 1.1, 1.2, 1.3, 1.4
    """
    
    SUPPORTED_FORMATS = {'wav', 'mp3', 'm4a'}
    MAX_DURATION_SECONDS = 5.0
    
    def __init__(self):
        """Initialize the audio input module"""
        if not PYDUB_AVAILABLE:
            raise ImportError(
                "pydub is required for audio processing. "
                "Install it with: pip install pydub"
            )
    
    def accept_recording(
        self, 
        audio_data: bytes, 
        format: str
    ) -> ValidationResult:
        """
        Accept audio recording from microphone.
        
        Args:
            audio_data: Raw audio bytes from microphone
            format: Audio format (e.g., 'wav', 'mp3', 'm4a')
            
        Returns:
            ValidationResult with validation status and audio data or error
            
        Requirements: 1.1
        """
        format_lower = format.lower().strip('.')
        
        # Validate format
        if format_lower not in self.SUPPORTED_FORMATS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Unsupported audio format: {format}. "
                             f"Supported formats: {', '.join(self.SUPPORTED_FORMATS).upper()}"
            )
        
        # Validate audio data
        return self._validate_audio_data(audio_data, format_lower)
    
    def accept_upload(self, file_data: bytes, filename: str) -> ValidationResult:
        """
        Accept uploaded audio file.
        
        Args:
            file_data: Audio file bytes
            filename: Original filename to extract format
            
        Returns:
            ValidationResult with validation status and audio data or error
            
        Requirements: 1.2
        """
        # Extract format from filename
        file_ext = os.path.splitext(filename)[1].lower().strip('.')
        
        if not file_ext:
            return ValidationResult(
                is_valid=False,
                error_message="Could not determine audio format from filename"
            )
        
        # Validate format
        if file_ext not in self.SUPPORTED_FORMATS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Unsupported audio format: {file_ext.upper()}. "
                             f"Supported formats: {', '.join(self.SUPPORTED_FORMATS).upper()}"
            )
        
        # Validate audio data
        return self._validate_audio_data(file_data, file_ext)
    
    def validate_audio(self, audio: AudioData) -> ValidationResult:
        """
        Validate an AudioData object.
        
        Args:
            audio: AudioData object to validate
            
        Returns:
            ValidationResult indicating if audio is valid
            
        Requirements: 1.3, 1.4
        """
        # Check format
        if audio.format.lower() not in self.SUPPORTED_FORMATS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid audio format: {audio.format}"
            )
        
        # Check duration
        if audio.duration_seconds > self.MAX_DURATION_SECONDS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Audio duration ({audio.duration_seconds:.1f}s) exceeds "
                             f"maximum allowed duration ({self.MAX_DURATION_SECONDS}s)"
            )
        
        return ValidationResult(
            is_valid=True,
            audio_data=audio
        )
    
    def _validate_audio_data(
        self, 
        audio_bytes: bytes, 
        format: str
    ) -> ValidationResult:
        """
        Internal method to validate raw audio bytes.
        
        Args:
            audio_bytes: Raw audio data
            format: Audio format string
            
        Returns:
            ValidationResult with validation status
            
        Requirements: 1.3, 1.4
        """
        if not audio_bytes:
            return ValidationResult(
                is_valid=False,
                error_message="Audio data is empty"
            )
        
        try:
            # Load audio using pydub
            audio_segment = AudioSegment.from_file(
                BytesIO(audio_bytes),
                format=format
            )
            
            # Get duration in seconds
            duration_seconds = len(audio_segment) / 1000.0
            
            # Validate duration (Requirement 1.3)
            if duration_seconds > self.MAX_DURATION_SECONDS:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Audio duration ({duration_seconds:.1f}s) exceeds "
                                 f"maximum allowed duration ({self.MAX_DURATION_SECONDS}s)"
                )
            
            # Get sample rate
            sample_rate = audio_segment.frame_rate
            
            # Create AudioData object
            audio_data = AudioData(
                data=audio_bytes,
                format=format,
                duration_seconds=duration_seconds,
                sample_rate=sample_rate
            )
            
            return ValidationResult(
                is_valid=True,
                audio_data=audio_data
            )
            
        except CouldntDecodeError:
            return ValidationResult(
                is_valid=False,
                error_message=f"Could not decode audio file. Please ensure it's a valid {format.upper()} file"
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Error processing audio: {str(e)}"
            )
    
    def get_audio_info(self, audio_bytes: bytes, format: str) -> Tuple[float, int]:
        """
        Get audio duration and sample rate without full validation.
        
        Args:
            audio_bytes: Raw audio data
            format: Audio format string
            
        Returns:
            Tuple of (duration_seconds, sample_rate)
            
        Raises:
            Exception if audio cannot be processed
        """
        audio_segment = AudioSegment.from_file(
            BytesIO(audio_bytes),
            format=format
        )
        duration_seconds = len(audio_segment) / 1000.0
        sample_rate = audio_segment.frame_rate
        return duration_seconds, sample_rate
