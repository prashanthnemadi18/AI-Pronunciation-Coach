"""
Unit tests for Audio Input Module

Tests audio validation, format checking, and duration limits.
"""

import pytest
from io import BytesIO
from pydub import AudioSegment
from pydub.generators import Sine
import subprocess

from app.modules.audio_input import AudioInputModule, AudioData, ValidationResult


def check_ffmpeg_available():
    """Check if ffmpeg is available for MP3 conversion"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


FFMPEG_AVAILABLE = check_ffmpeg_available()
requires_ffmpeg = pytest.mark.skipif(not FFMPEG_AVAILABLE, reason="ffmpeg not installed")


class TestAudioInputModule:
    """Test suite for AudioInputModule"""
    
    @pytest.fixture
    def audio_module(self):
        """Create AudioInputModule instance"""
        return AudioInputModule()
    
    @pytest.fixture
    def valid_wav_audio(self):
        """Generate valid WAV audio (2 seconds)"""
        # Generate 2 second sine wave at 440Hz
        audio = Sine(440).to_audio_segment(duration=2000)
        buffer = BytesIO()
        audio.export(buffer, format='wav')
        return buffer.getvalue()
    
    @pytest.fixture
    def long_wav_audio(self):
        """Generate WAV audio exceeding 5 seconds (6 seconds)"""
        audio = Sine(440).to_audio_segment(duration=6000)
        buffer = BytesIO()
        audio.export(buffer, format='wav')
        return buffer.getvalue()
    
    @pytest.fixture
    def valid_mp3_audio(self):
        """Generate valid MP3 audio (3 seconds)"""
        if not FFMPEG_AVAILABLE:
            pytest.skip("ffmpeg not available")
        audio = Sine(440).to_audio_segment(duration=3000)
        buffer = BytesIO()
        audio.export(buffer, format='mp3', bitrate='128k')
        return buffer.getvalue()
    
    # Test accept_recording method
    
    def test_accept_recording_valid_wav(self, audio_module, valid_wav_audio):
        """Test accepting valid WAV recording"""
        result = audio_module.accept_recording(valid_wav_audio, 'wav')
        
        assert result.is_valid is True
        assert result.error_message is None
        assert result.audio_data is not None
        assert result.audio_data.format == 'wav'
        assert result.audio_data.duration_seconds <= 5.0
    
    @requires_ffmpeg
    def test_accept_recording_valid_mp3(self, audio_module, valid_mp3_audio):
        """Test accepting valid MP3 recording"""
        result = audio_module.accept_recording(valid_mp3_audio, 'mp3')
        
        assert result.is_valid is True
        assert result.error_message is None
        assert result.audio_data is not None
        assert result.audio_data.format == 'mp3'
    
    def test_accept_recording_unsupported_format(self, audio_module, valid_wav_audio):
        """Test rejecting unsupported format"""
        result = audio_module.accept_recording(valid_wav_audio, 'ogg')
        
        assert result.is_valid is False
        assert 'Unsupported audio format' in result.error_message
        assert result.audio_data is None
    
    def test_accept_recording_exceeds_duration(self, audio_module, long_wav_audio):
        """Test rejecting audio exceeding 5 seconds (Requirement 1.3)"""
        result = audio_module.accept_recording(long_wav_audio, 'wav')
        
        assert result.is_valid is False
        assert 'exceeds maximum allowed duration' in result.error_message
        assert '5' in result.error_message
        assert result.audio_data is None
    
    def test_accept_recording_empty_data(self, audio_module):
        """Test rejecting empty audio data"""
        result = audio_module.accept_recording(b'', 'wav')
        
        assert result.is_valid is False
        assert 'empty' in result.error_message.lower()
        assert result.audio_data is None
    
    def test_accept_recording_format_case_insensitive(self, audio_module, valid_wav_audio):
        """Test format validation is case-insensitive"""
        result1 = audio_module.accept_recording(valid_wav_audio, 'WAV')
        result2 = audio_module.accept_recording(valid_wav_audio, 'Wav')
        result3 = audio_module.accept_recording(valid_wav_audio, 'wav')
        
        assert result1.is_valid is True
        assert result2.is_valid is True
        assert result3.is_valid is True
    
    # Test accept_upload method
    
    def test_accept_upload_valid_wav(self, audio_module, valid_wav_audio):
        """Test accepting valid WAV file upload (Requirement 1.2)"""
        result = audio_module.accept_upload(valid_wav_audio, 'recording.wav')
        
        assert result.is_valid is True
        assert result.error_message is None
        assert result.audio_data is not None
        assert result.audio_data.format == 'wav'
    
    @requires_ffmpeg
    def test_accept_upload_valid_mp3(self, audio_module, valid_mp3_audio):
        """Test accepting valid MP3 file upload"""
        result = audio_module.accept_upload(valid_mp3_audio, 'audio.mp3')
        
        assert result.is_valid is True
        assert result.audio_data.format == 'mp3'
    
    def test_accept_upload_unsupported_format(self, audio_module, valid_wav_audio):
        """Test rejecting unsupported file format (Requirement 1.4)"""
        result = audio_module.accept_upload(valid_wav_audio, 'audio.flac')
        
        assert result.is_valid is False
        assert 'Unsupported audio format' in result.error_message
    
    def test_accept_upload_no_extension(self, audio_module, valid_wav_audio):
        """Test rejecting file without extension"""
        result = audio_module.accept_upload(valid_wav_audio, 'audiofile')
        
        assert result.is_valid is False
        assert 'Could not determine audio format' in result.error_message
    
    def test_accept_upload_exceeds_duration(self, audio_module, long_wav_audio):
        """Test rejecting uploaded file exceeding duration limit"""
        result = audio_module.accept_upload(long_wav_audio, 'long.wav')
        
        assert result.is_valid is False
        assert 'exceeds maximum allowed duration' in result.error_message
    
    # Test validate_audio method
    
    def test_validate_audio_valid(self, audio_module):
        """Test validating valid AudioData object"""
        audio_data = AudioData(
            data=b'fake_audio_data',
            format='wav',
            duration_seconds=3.5,
            sample_rate=16000
        )
        
        result = audio_module.validate_audio(audio_data)
        
        assert result.is_valid is True
        assert result.audio_data == audio_data
    
    def test_validate_audio_invalid_format(self, audio_module):
        """Test rejecting invalid format in AudioData"""
        audio_data = AudioData(
            data=b'fake_audio_data',
            format='ogg',
            duration_seconds=3.0,
            sample_rate=16000
        )
        
        result = audio_module.validate_audio(audio_data)
        
        assert result.is_valid is False
        assert 'Invalid audio format' in result.error_message
    
    def test_validate_audio_exceeds_duration(self, audio_module):
        """Test rejecting AudioData exceeding duration limit"""
        audio_data = AudioData(
            data=b'fake_audio_data',
            format='wav',
            duration_seconds=6.5,
            sample_rate=16000
        )
        
        result = audio_module.validate_audio(audio_data)
        
        assert result.is_valid is False
        assert 'exceeds maximum allowed duration' in result.error_message
    
    def test_validate_audio_exactly_5_seconds(self, audio_module):
        """Test accepting audio exactly at 5 second limit"""
        audio_data = AudioData(
            data=b'fake_audio_data',
            format='wav',
            duration_seconds=5.0,
            sample_rate=16000
        )
        
        result = audio_module.validate_audio(audio_data)
        
        assert result.is_valid is True
    
    # Test edge cases
    
    def test_corrupted_audio_data(self, audio_module):
        """Test handling corrupted audio data"""
        corrupted_data = b'not_real_audio_data_just_random_bytes'
        result = audio_module.accept_recording(corrupted_data, 'wav')
        
        assert result.is_valid is False
        assert 'Could not decode' in result.error_message or 'Error processing' in result.error_message
    
    def test_supported_formats_constant(self, audio_module):
        """Test that all supported formats are documented"""
        assert 'wav' in audio_module.SUPPORTED_FORMATS
        assert 'mp3' in audio_module.SUPPORTED_FORMATS
        assert 'm4a' in audio_module.SUPPORTED_FORMATS
    
    def test_max_duration_constant(self, audio_module):
        """Test max duration is set to 5 seconds"""
        assert audio_module.MAX_DURATION_SECONDS == 5.0
    
    def test_get_audio_info(self, audio_module, valid_wav_audio):
        """Test getting audio information"""
        duration, sample_rate = audio_module.get_audio_info(valid_wav_audio, 'wav')
        
        assert duration > 0
        assert duration <= 5.0
        assert sample_rate > 0
    
    # Test all supported formats
    
    @requires_ffmpeg
    def test_all_supported_formats(self, audio_module):
        """Test that WAV, MP3, and M4A are all supported (Requirement 1.4)"""
        audio = Sine(440).to_audio_segment(duration=1000)
        
        # Test WAV
        buffer_wav = BytesIO()
        audio.export(buffer_wav, format='wav')
        result_wav = audio_module.accept_recording(buffer_wav.getvalue(), 'wav')
        assert result_wav.is_valid is True
        
        # Test MP3
        buffer_mp3 = BytesIO()
        audio.export(buffer_mp3, format='mp3')
        result_mp3 = audio_module.accept_recording(buffer_mp3.getvalue(), 'mp3')
        assert result_mp3.is_valid is True
