"""
Basic tests for ImageDetector module.

Tests module initialization, validation, and basic functionality.
"""

import pytest
from io import BytesIO
from PIL import Image
from image_detector import ImageDetector, DetectionResult


class TestImageDetector:
    """Basic tests for image detection functionality."""
    
    def test_initialization_with_gemini(self):
        """Test ImageDetector initialization with Gemini provider."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        assert detector.api_provider == 'gemini'
        assert detector.api_key == 'test_key'
    
    def test_initialization_invalid_provider(self):
        """Test that invalid provider raises error."""
        with pytest.raises(ValueError, match="Unsupported detection provider"):
            ImageDetector(api_provider='invalid_provider', api_key='test_key')
    
    def test_initialization_missing_api_key(self):
        """Test that missing API key for Gemini raises error."""
        with pytest.raises(ValueError, match="Gemini API key is required"):
            ImageDetector(api_provider='gemini', api_key='')
    
    def test_get_primary_object(self):
        """Test selecting primary object from detections."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        detections = [
            ("apple", 0.95),
            ("banana", 0.87),
            ("orange", 0.72)
        ]
        
        primary = detector.get_primary_object(detections)
        assert primary == "apple"  # Highest confidence
    
    def test_get_primary_object_single_detection(self):
        """Test primary object selection with single detection."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        detections = [("dog", 0.92)]
        primary = detector.get_primary_object(detections)
        assert primary == "dog"
    
    def test_get_primary_object_empty_list(self):
        """Test that empty detection list raises error."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        with pytest.raises(ValueError, match="No detections provided"):
            detector.get_primary_object([])
    
    def test_detect_object_invalid_image(self):
        """Test that invalid image data raises error."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        invalid_data = b"not an image"
        
        with pytest.raises(ValueError, match="Invalid image data"):
            detector.detect_object(invalid_data)
    
    def test_extract_object_name(self):
        """Test object name extraction from API response."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        # Test various response formats
        assert detector._extract_object_name("apple") == "apple"
        assert detector._extract_object_name("Apple.") == "apple"
        assert detector._extract_object_name('"dog"') == "dog"
        assert detector._extract_object_name("The cat") == "cat"
        assert detector._extract_object_name("a banana") == "banana"
        assert detector._extract_object_name("It is an orange") == "orange"
    
    def test_yolo_not_implemented(self):
        """Test that YOLO provider raises NotImplementedError."""
        detector = ImageDetector(api_provider='yolo', api_key='test_key')
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        with pytest.raises(NotImplementedError, match="YOLO detection not yet implemented"):
            detector.detect_object(img_bytes.read())
    
    def test_detection_result_structure(self):
        """Test DetectionResult data class structure."""
        result = DetectionResult(
            primary_object="apple",
            confidence=0.95,
            all_objects=[("apple", 0.95), ("fruit", 0.87)]
        )
        
        assert result.primary_object == "apple"
        assert result.confidence == 0.95
        assert len(result.all_objects) == 2
        assert result.all_objects[0] == ("apple", 0.95)
    
    def test_valid_image_validation(self):
        """Test that valid images pass validation."""
        detector = ImageDetector(api_provider='gemini', api_key='test_key')
        
        # Create a valid test image
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        image_data = img_bytes.read()
        
        # This should validate the image (will fail at API call, but that's expected)
        # We're just testing that it doesn't raise ValueError for invalid image
        try:
            detector.detect_object(image_data)
        except ValueError as e:
            # Should not be "Invalid image data" error
            assert "Invalid image data" not in str(e)
        except Exception:
            # Other exceptions (like API errors) are expected
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
