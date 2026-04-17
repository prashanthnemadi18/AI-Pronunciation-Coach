# Image Detector Module

## Overview

The Image Detector module identifies objects in images for the Image Mode pronunciation practice feature. It uses the Gemini Vision API to detect the primary object in an uploaded image, which then becomes the target word for pronunciation evaluation.

## Features

- **Object Detection**: Identifies objects in images using Gemini Vision API
- **Primary Object Selection**: Selects the most prominent object when multiple objects are detected
- **Confidence Scoring**: Returns confidence scores for detected objects
- **Image Validation**: Validates image data before processing
- **Error Handling**: Provides descriptive error messages for invalid images or API failures

## Requirements Coverage

- **Requirement 8.2**: Detect primary object in images
- **Requirement 8.3**: Set detected object name as target word

## Installation

The module requires the following dependencies:

```bash
pip install requests pillow
```

For Gemini Vision API access, you need a Gemini API key:
1. Visit https://makersuite.google.com/app/apikey
2. Create an API key
3. Set the environment variable: `export GEMINI_API_KEY=your_api_key`

## Usage

### Basic Usage

```python
from image_detector import ImageDetector

# Initialize detector with Gemini Vision API
detector = ImageDetector(api_provider='gemini', api_key='your_api_key')

# Or use environment variable
detector = ImageDetector(api_provider='gemini')  # Uses GEMINI_API_KEY env var

# Load image from file
with open('path/to/image.jpg', 'rb') as f:
    image_data = f.read()

# Detect object in image
result = detector.detect_object(image_data, filename='image.jpg')

# Access results
print(f"Primary object: {result.primary_object}")
print(f"Confidence: {result.confidence:.2f}")
print(f"All objects: {result.all_objects}")
```

### Selecting Primary Object

```python
# If you have multiple detections
detections = [
    ("apple", 0.95),
    ("banana", 0.87),
    ("orange", 0.72)
]

primary = detector.get_primary_object(detections)
print(f"Primary object: {primary}")  # Output: apple
```

### Error Handling

```python
try:
    result = detector.detect_object(image_data)
    print(f"Detected: {result.primary_object}")
except ValueError as e:
    print(f"Invalid image: {e}")
except Exception as e:
    print(f"Detection failed: {e}")
```

## API Reference

### ImageDetector Class

#### `__init__(api_provider: str = "gemini", api_key: Optional[str] = None)`

Initialize the image detector.

**Parameters:**
- `api_provider` (str): Detection provider ('gemini' or 'yolo'). Default: 'gemini'
- `api_key` (Optional[str]): API key for Gemini. If not provided, uses GEMINI_API_KEY environment variable

**Raises:**
- `ValueError`: If provider is not supported or API key is missing

#### `detect_object(image_data: bytes, filename: str = "image") -> DetectionResult`

Detect objects in the provided image.

**Parameters:**
- `image_data` (bytes): Image file data as bytes
- `filename` (str): Optional filename for context

**Returns:**
- `DetectionResult`: Object with primary_object, confidence, and all_objects

**Raises:**
- `ValueError`: If image is invalid or detection fails
- `Exception`: If API call fails

#### `get_primary_object(detections: List[Tuple[str, float]]) -> str`

Select the most prominent object from multiple detections.

**Parameters:**
- `detections` (List[Tuple[str, float]]): List of (object_name, confidence) tuples

**Returns:**
- `str`: Name of the primary object (highest confidence)

**Raises:**
- `ValueError`: If no detections provided

### DetectionResult Class

Data class containing detection results.

**Attributes:**
- `primary_object` (str): Name of the primary detected object
- `confidence` (float): Confidence score (0.0 to 1.0)
- `all_objects` (List[Tuple[str, float]]): List of all detected objects with confidence scores

## Integration with Pronunciation Coach

The Image Detector integrates into the pronunciation coach workflow:

1. **User uploads image** in Image Mode
2. **ImageDetector identifies** the primary object
3. **Object name becomes** the target word
4. **User pronounces** the word
5. **System evaluates** pronunciation using the standard pipeline

### Example Integration

```python
from image_detector import ImageDetector
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine
from feedback_generator import FeedbackGenerator

# Initialize modules
detector = ImageDetector(api_provider='gemini')
analyzer = PhonemeAnalyzer()
scorer = ScoringEngine()
feedback_gen = FeedbackGenerator('gemini', api_key)

# Step 1: Detect object in uploaded image
with open('user_image.jpg', 'rb') as f:
    image_data = f.read()

detection = detector.detect_object(image_data)
target_word = detection.primary_object

print(f"Please pronounce: {target_word}")

# Step 2: User records pronunciation (audio_data)
# ... audio recording logic ...

# Step 3: Evaluate pronunciation
# ... speech recognition to get transcribed_text ...

expected = analyzer.get_expected_phonemes(target_word)
actual = analyzer.get_actual_phonemes(transcribed_text)
comparison = analyzer.compare_phonemes(expected, actual)
score_result = scorer.calculate_score(comparison)
feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)

print(f"Score: {score_result.accuracy_score:.1f}/100")
print(f"Feedback: {feedback.correction_tips}")
```

## Supported Image Formats

The module supports common image formats:
- JPEG/JPG
- PNG
- GIF
- BMP
- WEBP

## Performance

- **API Timeout**: 5 seconds for detection requests
- **Image Validation**: Validates image before sending to API
- **Response Time**: Typically 1-3 seconds depending on image size and API latency

## Error Messages

Common error scenarios:

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid image data" | Corrupted or invalid image file | Verify image file is valid |
| "Gemini API key is required" | Missing API key | Set GEMINI_API_KEY environment variable |
| "No object detected in image" | API couldn't identify objects | Try a clearer image with distinct objects |
| "Gemini API error" | API request failed | Check API key and network connection |

## Future Enhancements

- **YOLO Integration**: Add support for local YOLO model for offline detection
- **Multiple Object Support**: Return multiple objects for user selection
- **Object Categories**: Filter objects by category (animals, food, vehicles, etc.)
- **Confidence Threshold**: Configurable minimum confidence for detection
- **Batch Processing**: Detect objects in multiple images at once

## Testing

Run the example usage script:

```bash
cd backend/app/modules
export GEMINI_API_KEY=your_api_key
python example_image_detector_usage.py
```

## License

Part of the AI Pronunciation Coach project.
