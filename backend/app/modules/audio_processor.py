"""
Audio Processing Module

Handles audio normalization, noise reduction, and format conversion
for optimal speech recognition performance.
"""

from dataclasses import dataclass
from typing import Optional
from io import BytesIO
import time

try:
    from pydub import AudioSegment
    from pydub.effects import normalize
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import librosa
    import numpy as np
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False


@dataclass
class ProcessedAudio:
    """Represents processed audio data ready for speech recognition"""
    data: bytes
    format: str
    duration_seconds: float
    sample_rate: int
    processing_time: float


@dataclass
class ProcessingResult:
    """Result of audio processing"""
    success: bool
    processed_audio: Optional[ProcessedAudio] = None
    error_message: Optional[str] = None


class AudioProcessor:
    """
    Handles audio processing including normalization, noise reduction,
    and format conversion for speech recognition.
    
    Requirements Coverage: 2.1, 2.2, 2.3, 2.4, 2.5
    """
    
    TARGET_SAMPLE_RATE = 16000  # Whisper expects 16kHz
    TARGET_FORMAT = 'wav'
    MAX_PROCESSING_TIME = 2.0  # seconds
    
    def __init__(self):
        """Initialize the audio processor"""
        if not PYDUB_AVAILABLE:
            raise ImportError(
                "pydub is required for audio processing. "
                "Install it with: pip install pydub"
            )
    
    def process(
        self, 
        audio_data: bytes, 
        source_format: str,
        duration_seconds: float
    ) -> ProcessingResult:
        """
        Process audio through full pipeline: normalize, denoise, convert format.
        
        Args:
            audio_data: Raw audio bytes
            source_format: Source audio format (e.g., 'wav', 'mp3', 'm4a')
            duration_seconds: Duration of the audio
            
        Returns:
            ProcessingResult with processed audio or error
            
        Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
        """
        start_time = time.time()
        
        try:
            # Load audio
            audio_segment = AudioSegment.from_file(
                BytesIO(audio_data),
                format=source_format
            )
            
            # Step 1: Normalize volume (Requirement 2.1)
            audio_segment = self.normalize_volume(audio_segment)
            
            # Step 2: Remove noise (Requirement 2.2)
            audio_segment = self.remove_noise(audio_segment)
            
            # Step 3: Convert format for Whisper (Requirement 2.3)
            audio_segment = self.convert_format(audio_segment)
            
            # Export processed audio
            output_buffer = BytesIO()
            audio_segment.export(
                output_buffer,
                format=self.TARGET_FORMAT,
                parameters=["-ar", str(self.TARGET_SAMPLE_RATE)]
            )
            processed_data = output_buffer.getvalue()
            
            processing_time = time.time() - start_time
            
            # Check processing time constraint (Requirement 2.5)
            if processing_time > self.MAX_PROCESSING_TIME:
                return ProcessingResult(
                    success=False,
                    error_message=f"Audio processing exceeded time limit "
                                 f"({processing_time:.2f}s > {self.MAX_PROCESSING_TIME}s)"
                )
            
            processed_audio = ProcessedAudio(
                data=processed_data,
                format=self.TARGET_FORMAT,
                duration_seconds=duration_seconds,
                sample_rate=self.TARGET_SAMPLE_RATE,
                processing_time=processing_time
            )
            
            return ProcessingResult(
                success=True,
                processed_audio=processed_audio
            )
            
        except Exception as e:
            # Requirement 2.4: Descriptive error messages
            return ProcessingResult(
                success=False,
                error_message=f"Audio processing failed: {str(e)}"
            )
    
    def normalize_volume(self, audio_segment: AudioSegment) -> AudioSegment:
        """
        Normalize audio volume to consistent level.
        
        Args:
            audio_segment: Input audio segment
            
        Returns:
            Normalized audio segment
            
        Requirements: 2.1
        """
        # Use pydub's normalize effect which applies peak normalization
        return normalize(audio_segment)
    
    def remove_noise(self, audio_segment: AudioSegment) -> AudioSegment:
        """
        Remove background noise from audio.
        
        Uses a simple high-pass filter to reduce low-frequency noise.
        For more advanced noise reduction, librosa could be used.
        
        Args:
            audio_segment: Input audio segment
            
        Returns:
            Denoised audio segment
            
        Requirements: 2.2
        """
        # Apply high-pass filter to remove low-frequency noise
        # This is a simple approach; more sophisticated methods exist
        filtered = audio_segment.high_pass_filter(200)
        
        # Optionally use librosa for more advanced noise reduction
        if LIBROSA_AVAILABLE:
            try:
                # Convert to numpy array for librosa processing
                samples = np.array(audio_segment.get_array_of_samples())
                sample_rate = audio_segment.frame_rate
                
                # Normalize to float
                if audio_segment.sample_width == 2:
                    samples = samples.astype(np.float32) / 32768.0
                elif audio_segment.sample_width == 4:
                    samples = samples.astype(np.float32) / 2147483648.0
                
                # Apply spectral gating for noise reduction
                # This is a simple approach - reduce very quiet parts
                threshold = np.percentile(np.abs(samples), 10)
                mask = np.abs(samples) > threshold
                samples = samples * mask
                
                # Convert back to audio segment
                if audio_segment.sample_width == 2:
                    samples = (samples * 32768.0).astype(np.int16)
                elif audio_segment.sample_width == 4:
                    samples = (samples * 2147483648.0).astype(np.int32)
                
                filtered = AudioSegment(
                    samples.tobytes(),
                    frame_rate=sample_rate,
                    sample_width=audio_segment.sample_width,
                    channels=audio_segment.channels
                )
            except Exception:
                # Fall back to simple filtering if librosa processing fails
                pass
        
        return filtered
    
    def convert_format(self, audio_segment: AudioSegment) -> AudioSegment:
        """
        Convert audio to format compatible with Whisper.
        
        Whisper expects:
        - 16kHz sample rate
        - Mono channel
        - WAV format
        
        Args:
            audio_segment: Input audio segment
            
        Returns:
            Converted audio segment
            
        Requirements: 2.3
        """
        # Convert to mono if stereo
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)
        
        # Set sample rate to 16kHz for Whisper
        if audio_segment.frame_rate != self.TARGET_SAMPLE_RATE:
            audio_segment = audio_segment.set_frame_rate(self.TARGET_SAMPLE_RATE)
        
        return audio_segment

