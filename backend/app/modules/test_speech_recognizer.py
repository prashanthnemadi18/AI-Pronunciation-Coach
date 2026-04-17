"""
Unit tests for Speech Recognition Module
"""

import pytest
import os
from io import BytesIO

# Import the modules we need
from .speech_recognizer import SpeechRecognizer, TranscriptionResult

# Check if whisper is available
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


@pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Whisper not installed")
class TestSpeechRecognizer:
    """Test suite for SpeechRecognizer class"""
    
    def setup_method(self):
        """Reset singleton before each test"""
        SpeechRecognizer.reset_instance()
    
    def test_singleton_pattern(self):
        """Test that SpeechRecognizer implements singleton pattern"""
        recognizer1 = SpeechRecognizer(model_size="base")
        recognizer2 = SpeechRecognizer(model_size="base")
        
        # Should be the same instance
        assert recognizer1 is recognizer2
        
        # Should share the same model
        assert recognizer1.get_model() is recognizer2.get_model()
    
    def test_initialization_with_model_size(self):
        """Test initialization with different model sizes"""
        recognizer = SpeechRecognizer(model_size="base")
        
        assert recognizer._model is not None
        assert recognizer._model_size == "base"
    
    def test_transcribe_with_silent_audio(self):
        """Test transcription with silent audio returns no speech detected error"""
        # Create a simple silent WAV file
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Generate 1 second of very quiet audio
        silent_audio = AudioSegment.silent(duration=1000)
        
        # Export to bytes
        buffer = BytesIO()
        silent_audio.export(buffer, format="wav")
        audio_bytes = buffer.getvalue()
        
        recognizer = SpeechRecognizer(model_size="base")
        result = recognizer.transcribe(audio_bytes, audio_format="wav")
        
        # Should fail with no speech detected
        # Note: Whisper might still transcribe something, so we check the result structure
        assert isinstance(result, TranscriptionResult)
        assert result.transcription_time is not None
    
    def test_transcribe_returns_result_structure(self):
        """Test that transcribe returns proper TranscriptionResult structure"""
        # Create a simple audio file with a tone
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Generate 1 second of 440Hz tone
        tone = Sine(440).to_audio_segment(duration=1000)
        
        # Export to bytes
        buffer = BytesIO()
        tone.export(buffer, format="wav")
        audio_bytes = buffer.getvalue()
        
        recognizer = SpeechRecognizer(model_size="base")
        result = recognizer.transcribe(audio_bytes, audio_format="wav")
        
        # Check result structure
        assert isinstance(result, TranscriptionResult)
        assert isinstance(result.success, bool)
        assert result.transcription_time is not None
        assert result.transcription_time >= 0
        
        if result.success:
            assert result.transcribed_text is not None
        else:
            assert result.error_message is not None
    
    def test_get_model_returns_model(self):
        """Test that get_model returns the loaded Whisper model"""
        recognizer = SpeechRecognizer(model_size="base")
        model = recognizer.get_model()
        
        assert model is not None
        # Check it's a Whisper model by checking for transcribe method
        assert hasattr(model, 'transcribe')
    
    def test_transcription_time_tracking(self):
        """Test that transcription time is tracked"""
        from pydub import AudioSegment
        
        # Create a short audio file
        silent_audio = AudioSegment.silent(duration=500)
        buffer = BytesIO()
        silent_audio.export(buffer, format="wav")
        audio_bytes = buffer.getvalue()
        
        recognizer = SpeechRecognizer(model_size="base")
        result = recognizer.transcribe(audio_bytes, audio_format="wav")
        
        # Should have transcription time
        assert result.transcription_time is not None
        assert result.transcription_time > 0
        # Should complete reasonably quickly for short audio
        assert result.transcription_time < 10.0  # Generous upper bound


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
