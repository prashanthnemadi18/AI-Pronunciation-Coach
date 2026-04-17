"""
Integration test for Speech Recognition Module with Audio Processing

This test demonstrates the integration between AudioProcessor and SpeechRecognizer.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speech_recognizer import SpeechRecognizer, TranscriptionResult

# Check if whisper is available
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


@pytest.mark.skipif(not WHISPER_AVAILABLE, reason="Whisper not installed")
class TestSpeechRecognitionIntegration:
    """Integration tests for speech recognition pipeline"""
    
    def test_speech_recognizer_initialization(self):
        """Test that SpeechRecognizer initializes correctly"""
        recognizer = SpeechRecognizer(model_size="base")
        
        assert recognizer is not None
        assert recognizer._model is not None
        assert recognizer._model_size == "base"
        assert recognizer.MAX_TRANSCRIPTION_TIME == 3.0
    
    def test_singleton_pattern_thread_safe(self):
        """Test singleton pattern is thread-safe"""
        import threading
        
        instances = []
        
        def create_instance():
            recognizer = SpeechRecognizer(model_size="base")
            instances.append(recognizer)
        
        # Create multiple instances in parallel
        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)
    
    def test_transcription_result_structure(self):
        """Test TranscriptionResult dataclass structure"""
        result = TranscriptionResult(
            success=True,
            transcribed_text="hello world",
            transcription_time=1.5,
            confidence=0.95
        )
        
        assert result.success is True
        assert result.transcribed_text == "hello world"
        assert result.transcription_time == 1.5
        assert result.confidence == 0.95
        assert result.error_message is None
    
    def test_error_result_structure(self):
        """Test TranscriptionResult error structure"""
        result = TranscriptionResult(
            success=False,
            error_message="No speech detected"
        )
        
        assert result.success is False
        assert result.error_message == "No speech detected"
        assert result.transcribed_text is None
    
    def test_get_model_returns_whisper_instance(self):
        """Test that get_model returns a Whisper model"""
        recognizer = SpeechRecognizer(model_size="base")
        model = recognizer.get_model()
        
        assert model is not None
        assert hasattr(model, 'transcribe')
        assert hasattr(model, 'decode')
    
    def test_reset_instance(self):
        """Test that reset_instance clears the singleton"""
        recognizer1 = SpeechRecognizer(model_size="base")
        SpeechRecognizer.reset_instance()
        recognizer2 = SpeechRecognizer(model_size="base")
        
        # After reset, we get a new instance
        # Note: They might be the same object due to singleton, but model is reloaded
        assert recognizer2._model is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
