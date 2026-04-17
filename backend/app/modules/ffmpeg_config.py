"""
FFmpeg Configuration Module

Sets up FFmpeg paths for pydub before any audio processing modules are imported.
This must be imported first in main.py to ensure FFmpeg is configured correctly.
"""

import os
from pathlib import Path

def configure_ffmpeg():
    """Configure FFmpeg paths for pydub"""
    # Get FFmpeg path from environment
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', r'D:\Hackathon2.O\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe')
    FFPROBE_PATH = FFMPEG_PATH.replace('ffmpeg.exe', 'ffprobe.exe') if FFMPEG_PATH.endswith('ffmpeg.exe') else None
    
    # Set environment variables for pydub
    if os.path.exists(FFMPEG_PATH):
        os.environ['FFMPEG_BINARY'] = FFMPEG_PATH
        if FFPROBE_PATH and os.path.exists(FFPROBE_PATH):
            os.environ['FFPROBE_BINARY'] = FFPROBE_PATH
        
        # Add to PATH
        ffmpeg_dir = str(Path(FFMPEG_PATH).parent)
        if ffmpeg_dir not in os.environ.get('PATH', ''):
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
    
    try:
        from pydub import AudioSegment
        
        if os.path.exists(FFMPEG_PATH):
            AudioSegment.converter = FFMPEG_PATH
            AudioSegment.ffmpeg = FFMPEG_PATH
            
            if FFPROBE_PATH and os.path.exists(FFPROBE_PATH):
                AudioSegment.ffprobe = FFPROBE_PATH
            
            return True
        else:
            return False
            
    except ImportError:
        return False
    except Exception as e:
        return False

# Auto-configure when module is imported
configure_ffmpeg()
