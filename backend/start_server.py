"""
Startup script for AI Pronunciation Coach API

This script helps start the FastAPI server with proper configuration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

# Set FFmpeg path in environment BEFORE any imports
FFMPEG_PATH = os.getenv('FFMPEG_PATH', r'D:\Hackathon2.O\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe')
if os.path.exists(FFMPEG_PATH):
    # Set environment variables that pydub will check
    os.environ['FFMPEG_BINARY'] = FFMPEG_PATH
    os.environ['FFPROBE_BINARY'] = FFMPEG_PATH.replace('ffmpeg.exe', 'ffprobe.exe')
    
    # Also add to PATH
    ffmpeg_dir = str(Path(FFMPEG_PATH).parent)
    if ffmpeg_dir not in os.environ['PATH']:
        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ['PATH']

def check_environment():
    """Check if required environment variables are set"""
    warnings = []
    
    # Check for LLM API key
    if not os.getenv('LLM_API_KEY') and not os.getenv('GEMINI_API_KEY'):
        warnings.append("⚠️  LLM_API_KEY or GEMINI_API_KEY not set - feedback generation will be unavailable")
    
    # Check for image detection API key
    if not os.getenv('GEMINI_API_KEY'):
        warnings.append("⚠️  GEMINI_API_KEY not set - image detection will be unavailable")
    
    return warnings

def main():
    """Main startup function"""
    print("=" * 60)
    print("AI Pronunciation Coach - Backend API")
    print("=" * 60)
    print()
    
    # Check environment
    warnings = check_environment()
    
    if warnings:
        print("Environment Warnings:")
        for warning in warnings:
            print(f"  {warning}")
        print()
        print("To enable all features, set the following environment variables:")
        print("  - GEMINI_API_KEY: For feedback generation and image detection")
        print("  - LLM_API_KEY: Alternative to GEMINI_API_KEY for feedback")
        print()
    
    # Check if running in development or production
    port = os.getenv('PORT', '8000')
    host = os.getenv('HOST', '0.0.0.0')
    reload = '--reload' if '--dev' in sys.argv else ''
    
    print(f"Starting server on {host}:{port}")
    print()
    print("Available endpoints:")
    print("  - POST /api/pronunciation/evaluate")
    print("  - POST /api/pronunciation/image")
    print("  - GET  /api/user/{user_id}/history")
    print("  - GET  /api/leaderboard")
    print("  - GET  /api/health")
    print()
    print("API Documentation:")
    print(f"  - Swagger UI: http://localhost:{port}/docs")
    print(f"  - ReDoc: http://localhost:{port}/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Start uvicorn
    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=int(port),
        reload='--dev' in sys.argv
    )

if __name__ == "__main__":
    main()
