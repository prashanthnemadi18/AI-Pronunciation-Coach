"""
Example usage of the Audio Processing Module

Demonstrates how to use the AudioProcessor class to process audio
for speech recognition.
"""

from pathlib import Path
from app.modules.audio_input import AudioInputModule
from app.modules.audio_processor import AudioProcessor


def main():
    """Example usage of AudioProcessor"""
    
    # Initialize modules
    audio_input = AudioInputModule()
    audio_processor = AudioProcessor()
    
    print("Audio Processing Module Example")
    print("=" * 50)
    
    # Example 1: Process audio from file upload
    print("\n1. Processing uploaded audio file...")
    
    # Simulate file upload (in real usage, this would come from a web request)
    # For this example, we'll create a simple test audio file
    try:
        # Read an audio file (you would need an actual audio file here)
        # audio_file_path = Path("test_audio.wav")
        # if audio_file_path.exists():
        #     with open(audio_file_path, 'rb') as f:
        #         file_data = f.read()
        #     
        #     # Validate with AudioInputModule
        #     validation_result = audio_input.accept_upload(file_data, "test_audio.wav")
        #     
        #     if validation_result.is_valid:
        #         audio_data = validation_result.audio_data
        #         print(f"   ✓ Audio validated: {audio_data.duration_seconds:.2f}s, {audio_data.format}")
        #         
        #         # Process the audio
        #         processing_result = audio_processor.process(
        #             audio_data=audio_data.data,
        #             source_format=audio_data.format,
        #             duration_seconds=audio_data.duration_seconds
        #         )
        #         
        #         if processing_result.success:
        #             processed = processing_result.processed_audio
        #             print(f"   ✓ Audio processed successfully!")
        #             print(f"     - Format: {processed.format}")
        #             print(f"     - Sample rate: {processed.sample_rate} Hz")
        #             print(f"     - Duration: {processed.duration_seconds:.2f}s")
        #             print(f"     - Processing time: {processed.processing_time:.3f}s")
        #         else:
        #             print(f"   ✗ Processing failed: {processing_result.error_message}")
        #     else:
        #         print(f"   ✗ Validation failed: {validation_result.error_message}")
        
        print("   (Skipped - no test audio file available)")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Example 2: Demonstrate processing pipeline
    print("\n2. Audio Processing Pipeline:")
    print("   Input Audio")
    print("      ↓")
    print("   [Normalize Volume]  ← Ensures consistent volume level")
    print("      ↓")
    print("   [Remove Noise]      ← Reduces background noise")
    print("      ↓")
    print("   [Convert Format]    ← Converts to 16kHz mono WAV for Whisper")
    print("      ↓")
    print("   Processed Audio (ready for speech recognition)")
    
    # Example 3: Show processing constraints
    print("\n3. Processing Constraints:")
    print(f"   - Target sample rate: {audio_processor.TARGET_SAMPLE_RATE} Hz")
    print(f"   - Target format: {audio_processor.TARGET_FORMAT.upper()}")
    print(f"   - Max processing time: {audio_processor.MAX_PROCESSING_TIME}s")
    print(f"   - Target channels: Mono (1 channel)")
    
    # Example 4: Error handling
    print("\n4. Error Handling:")
    print("   The AudioProcessor provides descriptive error messages:")
    
    # Test with invalid audio
    result = audio_processor.process(
        audio_data=b'invalid data',
        source_format='wav',
        duration_seconds=1.0
    )
    
    if not result.success:
        print(f"   ✓ Error caught: {result.error_message}")
    
    print("\n" + "=" * 50)
    print("Example complete!")


if __name__ == '__main__':
    main()

