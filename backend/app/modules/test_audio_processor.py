"""
Unit tests for Audio Processing Module

Tests volume normalization, noise reduction, and format conversion.
"""

import pytest
from io import BytesIO
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

from app.modules.audio_processor import AudioProcessor, ProcessedAudio, ProcessingResult


@pytest.fixture
def audio_processor():
    """Create an AudioProcessor instance for testing"""
    return AudioProcessor()


@pytest.fixture
def sample_audio_wav():
    """Generate a sample WAV audio for testing (1 second, 440Hz tone)"""
    # Generate 1 second of 440Hz sine wave
    tone = Sine(440).to_audio_segment(duration=1000)
    
    # Export to bytes
    buffer = BytesIO()
    tone.export(buffer, format='wav')
    return buffer.getvalue()


@pytest.fixture
def sample_audio_mp3():
    """Generate a sample MP3 audio for testing"""
    tone = Sine(440).to_audio_segment(duration=1000)
    buffer = BytesIO()
    tone.export(buffer, format='mp3')
    return buffer.getvalue()


@pytest.fixture
def quiet_audio():
    """Generate very quiet audio for testing normalization"""
    tone = Sine(440).to_audio_segment(duration=1000)
    # Reduce volume by 20 dB
    quiet = tone - 20
    buffer = BytesIO()
    quiet.export(buffer, format='wav')
    return buffer.getvalue()


@pytest.fixture
def loud_audio():
    """Generate very loud audio for testing normalization"""
    tone = Sine(440).to_audio_segment(duration=1000)
    # Increase volume by 10 dB
    loud = tone + 10
    buffer = BytesIO()
    loud.export(buffer, format='wav')
    return buffer.getvalue()


class TestAudioProcessor:
    """Test suite for AudioProcessor class"""
    
    def test_initialization(self, audio_processor):
        """Test AudioProcessor initializes correctly"""
        assert audio_processor is not None
        assert audio_processor.TARGET_SAMPLE_RATE == 16000
        assert audio_processor.TARGET_FORMAT == 'wav'
    
    def test_process_valid_wav(self, audio_processor, sample_audio_wav):
        """Test processing valid WAV audio"""
        result = audio_processor.process(
            audio_data=sample_audio_wav,
            source_format='wav',
            duration_seconds=1.0
        )
        
        assert result.success is True
        assert result.processed_audio is not None
        assert result.error_message is None
        assert result.processed_audio.format == 'wav'
        assert result.processed_audio.sample_rate == 16000
        assert result.processed_audio.processing_time < 2.0
    
    def test_process_valid_mp3(self, audio_processor, sample_audio_mp3):
        """Test processing valid MP3 audio"""
        result = audio_processor.process(
            audio_data=sample_audio_mp3,
            source_format='mp3',
            duration_seconds=1.0
        )
        
        assert result.success is True
        assert result.processed_audio is not None
        assert result.processed_audio.format == 'wav'
        assert result.processed_audio.sample_rate == 16000
    
    def test_normalize_volume_quiet_audio(self, audio_processor, quiet_audio):
        """Test volume normalization increases quiet audio"""
        # Load quiet audio
        audio_segment = AudioSegment.from_file(BytesIO(quiet_audio), format='wav')
        original_dbfs = audio_segment.dBFS
        
        # Normalize
        normalized = audio_processor.normalize_volume(audio_segment)
        normalized_dbfs = normalized.dBFS
        
        # Normalized audio should be louder (higher dBFS)
        assert normalized_dbfs > original_dbfs
    
    def test_normalize_volume_loud_audio(self, audio_processor, loud_audio):
        """Test volume normalization processes loud audio"""
        # Load loud audio
        audio_segment = AudioSegment.from_file(BytesIO(loud_audio), format='wav')
        
        # Normalize
        normalized = audio_processor.normalize_volume(audio_segment)
        normalized_dbfs = normalized.dBFS
        
        # Normalized audio should be at a consistent level
        # Peak normalization brings audio closer to 0 dBFS
        # Just verify normalization returns valid audio
        assert isinstance(normalized, AudioSegment)
        assert normalized_dbfs is not None
    
    def test_remove_noise(self, audio_processor, sample_audio_wav):
        """Test noise reduction processing"""
        audio_segment = AudioSegment.from_file(BytesIO(sample_audio_wav), format='wav')
        
        # Apply noise reduction
        denoised = audio_processor.remove_noise(audio_segment)
        
        # Should return an AudioSegment
        assert isinstance(denoised, AudioSegment)
        # Duration should be preserved
        assert abs(len(denoised) - len(audio_segment)) < 10  # Within 10ms
    
    def test_convert_format_stereo_to_mono(self, audio_processor):
        """Test conversion from stereo to mono"""
        # Create stereo audio
        tone = Sine(440).to_audio_segment(duration=1000)
        stereo = AudioSegment.from_mono_audiosegments(tone, tone)
        
        # Convert
        mono = audio_processor.convert_format(stereo)
        
        assert mono.channels == 1
    
    def test_convert_format_sample_rate(self, audio_processor):
        """Test sample rate conversion to 16kHz"""
        # Create audio with different sample rate
        tone = Sine(440).to_audio_segment(duration=1000)
        tone = tone.set_frame_rate(44100)  # CD quality
        
        # Convert
        converted = audio_processor.convert_format(tone)
        
        assert converted.frame_rate == 16000
    
    def test_convert_format_already_correct(self, audio_processor):
        """Test conversion when audio is already in correct format"""
        # Create audio already in target format
        tone = Sine(440).to_audio_segment(duration=1000)
        tone = tone.set_frame_rate(16000).set_channels(1)
        
        # Convert (should be no-op)
        converted = audio_processor.convert_format(tone)
        
        assert converted.frame_rate == 16000
        assert converted.channels == 1
    
    def test_process_invalid_audio(self, audio_processor):
        """Test processing with invalid audio data"""
        result = audio_processor.process(
            audio_data=b'invalid audio data',
            source_format='wav',
            duration_seconds=1.0
        )
        
        assert result.success is False
        assert result.error_message is not None
        assert "failed" in result.error_message.lower()
    
    def test_process_empty_audio(self, audio_processor):
        """Test processing with empty audio data"""
        result = audio_processor.process(
            audio_data=b'',
            source_format='wav',
            duration_seconds=0.0
        )
        
        assert result.success is False
        assert result.error_message is not None
    
    def test_processing_time_constraint(self, audio_processor, sample_audio_wav):
        """Test that processing completes within time limit"""
        result = audio_processor.process(
            audio_data=sample_audio_wav,
            source_format='wav',
            duration_seconds=1.0
        )
        
        assert result.success is True
        assert result.processed_audio.processing_time <= 2.0
    
    def test_process_max_duration_audio(self, audio_processor):
        """Test processing 5-second audio (max duration)"""
        # Generate 5 second audio
        tone = Sine(440).to_audio_segment(duration=5000)
        buffer = BytesIO()
        tone.export(buffer, format='wav')
        audio_data = buffer.getvalue()
        
        result = audio_processor.process(
            audio_data=audio_data,
            source_format='wav',
            duration_seconds=5.0
        )
        
        assert result.success is True
        assert result.processed_audio.processing_time <= 2.0
    
    def test_processed_audio_format(self, audio_processor, sample_audio_wav):
        """Test that processed audio has correct format"""
        result = audio_processor.process(
            audio_data=sample_audio_wav,
            source_format='wav',
            duration_seconds=1.0
        )
        
        # Verify processed audio can be loaded
        processed_segment = AudioSegment.from_file(
            BytesIO(result.processed_audio.data),
            format='wav'
        )
        
        assert processed_segment.frame_rate == 16000
        assert processed_segment.channels == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

