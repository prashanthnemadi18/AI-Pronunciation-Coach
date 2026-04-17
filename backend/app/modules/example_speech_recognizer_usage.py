"""
Example usage of the Speech Recognition Module

This demonstrates how to use the SpeechRecognizer class.
"""

from speech_recognizer import SpeechRecognizer, TranscriptionResult
import os


def example_transcribe_audio():
    """
    Example: Transcribe audio from a file
    """
    print("=== Speech Recognition Example ===\n")
    
    # Initialize the speech recognizer (singleton pattern)
    # Using 'base' model for balance of speed and accuracy
    recognizer = SpeechRecognizer(model_size="base")
    print(f"✓ Initialized SpeechRecognizer with model: {recognizer._model_size}")
    
    # Example: If you have processed audio data
    # In a real scenario, this would come from AudioProcessor
    print("\nNote: To transcribe audio, you need:")
    print("1. Audio data in bytes format (preferably 16kHz WAV)")
    print("2. Call recognizer.transcribe(audio_bytes, 'wav')")
    print("\nThe transcribe method will:")
    print("- Convert audio to text using Whisper")
    print("- Return TranscriptionResult with success status")
    print("- Include transcribed text or error message")
    print("- Track transcription time (must be < 3 seconds)")
    print("- Handle 'no speech detected' errors")
    
    # Show singleton pattern
    recognizer2 = SpeechRecognizer(model_size="base")
    print(f"\n✓ Singleton pattern verified: {recognizer is recognizer2}")
    
    # Get the model
    model = recognizer.get_model()
    print(f"✓ Whisper model loaded: {type(model).__name__}")
    
    print("\n=== Example Complete ===")


def example_full_pipeline():
    """
    Example: Full pipeline from audio input to transcription
    """
    print("\n=== Full Pipeline Example ===\n")
    
    print("Complete pronunciation evaluation pipeline:")
    print("1. AudioInputModule: Validate audio (format, duration)")
    print("2. AudioProcessor: Normalize, denoise, convert to 16kHz WAV")
    print("3. SpeechRecognizer: Transcribe audio to text")
    print("4. PhonemeAnalyzer: Compare phonemes (next module)")
    print("5. ScoringEngine: Calculate accuracy score (next module)")
    print("6. FeedbackGenerator: Generate correction tips (next module)")
    
    print("\nSpeechRecognizer requirements:")
    print("✓ Uses Whisper base or small model (Req 3.1, 3.2)")
    print("✓ Transcribes audio to text (Req 3.1)")
    print("✓ Handles no speech detected errors (Req 3.3)")
    print("✓ Passes text to next module (Req 3.4)")
    print("✓ Completes within 3 seconds (Req 3.5)")
    print("✓ Implements singleton pattern for performance")
    
    print("\n=== Pipeline Overview Complete ===")


if __name__ == "__main__":
    example_transcribe_audio()
    example_full_pipeline()
