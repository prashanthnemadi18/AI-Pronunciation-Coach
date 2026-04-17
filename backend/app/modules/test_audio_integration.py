"""
Integration test for Audio Input and Audio Processing modules

Tests the integration between AudioInputModule and AudioProcessor.
"""

import pytest
from io import BytesIO
from pydub import AudioSegment
from pydub.generators import Sine

from app.modules.audio_input import AudioInputModule
from app.modules.audio_processor import AudioProcessor


@pytest.fixture
def audio_input_module():
    """Create an AudioInputModule instance"""
    return AudioInputModule()


@pytest.fixture
def audio_processor():
    """Create an AudioProcessor instance"""
    return AudioProcessor()


@pytest.fixture
def sample_wav_file():
    """Generate a sample WAV file for testing"""
    # Generate 2 second audio
    tone = Sine(440).to_audio_segment(duration=2000)
    buffer = BytesIO()
    tone.export(buffer, format='wav')
    return buffer.getvalue()


class TestAudioIntegration:
    """Integration tests for audio input and processing pipeline"""
    
    def test_full_pipeline_upload(self, audio_input_module, audio_processor, sample_wav_file):
        """Test complete pipeline: upload → validate → process"""
        
        # Step 1: Accept upload
        validation_result = audio_input_module.accept_upload(
            file_data=sample_wav_file,
            filename="test.wav"
        )
        
        assert validation_result.is_valid is True
        assert validation_result.audio_data is not None
        
        audio_data = validation_result.audio_data
        
        # Step 2: Process audio
        processing_result = audio_processor.process(
            audio_data=audio_data.data,
            source_format=audio_data.format,
            duration_seconds=audio_data.duration_seconds
        )
        
        assert processing_result.success is True
        assert processing_result.processed_audio is not None
        
        processed = processing_result.processed_audio
        
        # Verify processed audio meets Whisper requirements
        assert processed.format == 'wav'
        assert processed.sample_rate == 16000
        assert processed.processing_time <= 2.0
    
    def test_full_pipeline_recording(self, audio_input_module, audio_processor, sample_wav_file):
        """Test complete pipeline: recording → validate → process"""
        
        # Step 1: Accept recording
        validation_result = audio_input_module.accept_recording(
            audio_data=sample_wav_file,
            format='wav'
        )
        
        assert validation_result.is_valid is True
        audio_data = validation_result.audio_data
        
        # Step 2: Process audio
        processing_result = audio_processor.process(
            audio_data=audio_data.data,
            source_format=audio_data.format,
            duration_seconds=audio_data.duration_seconds
        )
        
        assert processing_result.success is True
        processed = processing_result.processed_audio
        
        # Verify output is ready for Whisper
        assert processed.sample_rate == 16000
        assert processed.format == 'wav'
    
    def test_pipeline_with_mp3(self, audio_input_module, audio_processor):
        """Test pipeline with MP3 input"""
        
        # Generate MP3 audio
        tone = Sine(440).to_audio_segment(duration=1000)
        buffer = BytesIO()
        tone.export(buffer, format='mp3')
        mp3_data = buffer.getvalue()
        
        # Validate
        validation_result = audio_input_module.accept_upload(
            file_data=mp3_data,
            filename="test.mp3"
        )
        
        assert validation_result.is_valid is True
        
        # Process
        audio_data = validation_result.audio_data
        processing_result = audio_processor.process(
            audio_data=audio_data.data,
            source_format=audio_data.format,
            duration_seconds=audio_data.duration_seconds
        )
        
        assert processing_result.success is True
        # MP3 should be converted to WAV
        assert processing_result.processed_audio.format == 'wav'
    
    def test_pipeline_rejects_long_audio(self, audio_input_module, audio_processor):
        """Test that pipeline rejects audio longer than 5 seconds"""
        
        # Generate 6 second audio (exceeds limit)
        tone = Sine(440).to_audio_segment(duration=6000)
        buffer = BytesIO()
        tone.export(buffer, format='wav')
        long_audio = buffer.getvalue()
        
        # Should be rejected at validation stage
        validation_result = audio_input_module.accept_upload(
            file_data=long_audio,
            filename="long.wav"
        )
        
        assert validation_result.is_valid is False
        assert "exceeds" in validation_result.error_message.lower()
    
    def test_pipeline_error_propagation(self, audio_input_module, audio_processor):
        """Test that errors propagate correctly through pipeline"""
        
        # Invalid audio data
        validation_result = audio_input_module.accept_upload(
            file_data=b'invalid',
            filename="test.wav"
        )
        
        # Should fail at validation
        assert validation_result.is_valid is False
        assert validation_result.error_message is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

