# Speech Recognition Module

## Overview

The Speech Recognition Module converts speech audio to text transcription using OpenAI Whisper. It implements a singleton pattern for efficient model loading and provides robust error handling.

## Features

- **Whisper Integration**: Uses OpenAI Whisper for accurate speech-to-text conversion
- **Singleton Pattern**: Efficient model loading with thread-safe singleton implementation
- **Performance Optimized**: Uses base model for balance of speed and accuracy
- **Error Handling**: Handles no speech detected, transcription failures, and time constraints
- **Time Tracking**: Monitors transcription time to ensure < 3 second constraint

## Requirements Coverage

| Requirement | Description | Implementation |
|------------|-------------|----------------|
| 3.1 | Initialize Whisper model (base or small size) | `DEFAULT_MODEL_SIZE = "base"` |
| 3.2 | Implement transcribe method | `transcribe()` method with Whisper API |
| 3.3 | Handle no speech detected errors | Checks for empty transcription |
| 3.4 | Pass transcribed text to next module | Returns `TranscriptionResult` |
| 3.5 | Complete within 3 seconds | `MAX_TRANSCRIPTION_TIME = 3.0` validation |

## Usage

### Basic Usage

```python
from speech_recognizer import SpeechRecognizer

# Initialize recognizer (singleton pattern)
recognizer = SpeechRecognizer(model_size="base")

# Transcribe audio
result = recognizer.transcribe(audio_bytes, audio_format="wav")

if result.success:
    print(f"Transcribed: {result.transcribed_text}")
    print(f"Time: {result.transcription_time:.2f}s")
else:
    print(f"Error: {result.error_message}")
```

### Full Pipeline Integration

```python
from audio_input import AudioInputModule
from audio_processor import AudioProcessor
from speech_recognizer import SpeechRecognizer

# Step 1: Validate audio input
audio_input = AudioInputModule()
validation = audio_input.accept_recording(audio_bytes, 'wav')

if validation.is_valid:
    # Step 2: Process audio
    processor = AudioProcessor()
    processed = processor.process(
        validation.audio_data.data,
        validation.audio_data.format,
        validation.audio_data.duration_seconds
    )
    
    if processed.success:
        # Step 3: Transcribe
        recognizer = SpeechRecognizer()
        result = recognizer.transcribe(
            processed.processed_audio.data,
            processed.processed_audio.format
        )
        
        if result.success:
            print(f"Transcription: {result.transcribed_text}")
```

## API Reference

### SpeechRecognizer Class

#### Constructor

```python
SpeechRecognizer(model_size: str = "base")
```

**Parameters:**
- `model_size` (str): Whisper model size. Options: 'tiny', 'base', 'small', 'medium', 'large'. Default: 'base'

**Note:** Uses singleton pattern - multiple instantiations return the same instance.

#### Methods

##### transcribe()

```python
transcribe(audio_data: bytes, audio_format: str = "wav") -> TranscriptionResult
```

Transcribe audio to text using Whisper.

**Parameters:**
- `audio_data` (bytes): Processed audio bytes (preferably 16kHz WAV)
- `audio_format` (str): Audio format. Default: 'wav'

**Returns:**
- `TranscriptionResult`: Result object with transcription or error

**Example:**
```python
result = recognizer.transcribe(audio_bytes, "wav")
```

##### get_model()

```python
get_model() -> whisper.Whisper
```

Get the loaded Whisper model instance.

**Returns:**
- Loaded Whisper model

##### reset_instance() (class method)

```python
SpeechRecognizer.reset_instance()
```

Reset singleton instance (useful for testing).

### TranscriptionResult Dataclass

```python
@dataclass
class TranscriptionResult:
    success: bool
    transcribed_text: Optional[str] = None
    error_message: Optional[str] = None
    transcription_time: Optional[float] = None
    confidence: Optional[float] = None
```

**Fields:**
- `success` (bool): Whether transcription succeeded
- `transcribed_text` (str, optional): Transcribed text if successful
- `error_message` (str, optional): Error message if failed
- `transcription_time` (float, optional): Time taken for transcription in seconds
- `confidence` (float, optional): Confidence score (0-1) if available

## Error Handling

The module handles several error conditions:

1. **No Speech Detected**: Returns error when audio contains no speech
   ```python
   TranscriptionResult(
       success=False,
       error_message="No speech detected in audio. Please speak more clearly."
   )
   ```

2. **Time Constraint Exceeded**: Returns error if transcription takes > 3 seconds
   ```python
   TranscriptionResult(
       success=False,
       error_message="Transcription exceeded time limit (3.5s > 3.0s)"
   )
   ```

3. **Transcription Failure**: Returns error for any other failures
   ```python
   TranscriptionResult(
       success=False,
       error_message="Transcription failed: [error details]"
   )
   ```

## Performance Considerations

- **Model Size**: Uses 'base' model by default for balance of speed and accuracy
  - 'tiny': Fastest, less accurate
  - 'base': Good balance (recommended)
  - 'small': More accurate, slower
  - 'medium'/'large': Most accurate, slowest

- **Singleton Pattern**: Model is loaded once and reused across all transcriptions
- **Time Constraint**: Enforces 3-second maximum transcription time
- **CPU Compatibility**: Uses `fp16=False` for CPU compatibility

## Testing

Run tests with:
```bash
pytest backend/app/modules/test_speech_recognizer.py -v
```

Run example:
```bash
python backend/app/modules/example_speech_recognizer_usage.py
```

## Dependencies

- `openai-whisper>=20231117`: Whisper speech recognition
- `torch`: PyTorch (required by Whisper)
- `numpy`: Numerical operations (required by Whisper)

Install with:
```bash
pip install openai-whisper
```

## Integration with Other Modules

### Input from AudioProcessor

The SpeechRecognizer expects processed audio from the AudioProcessor:
- Format: WAV
- Sample Rate: 16kHz
- Channels: Mono

### Output to PhonemeAnalyzer

The transcribed text is passed to the PhonemeAnalyzer for phoneme comparison:
```python
if transcription_result.success:
    phoneme_analyzer.get_actual_phonemes(transcription_result.transcribed_text)
```

## Notes

- The module uses temporary files for Whisper processing (automatically cleaned up)
- Thread-safe singleton implementation for concurrent access
- Optimized for English language transcription
- Confidence scores are calculated from Whisper's no_speech_prob metric
