"""
Image Detection Module

Detects objects in images for Image Mode pronunciation practice.
Uses Gemini Vision API or YOLO for object detection.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import base64
import requests
import os
from io import BytesIO
from PIL import Image


@dataclass
class DetectionResult:
    """Result of image object detection"""
    primary_object: str
    confidence: float
    all_objects: List[Tuple[str, float]]  # (object, confidence)


class ImageDetector:
    """
    Detects objects in images using Gemini Vision API or YOLO.
    
    Returns the primary object name as the target word for pronunciation practice.
    Handles multiple objects by selecting the most prominent one.
    
    Requirements Coverage: 8.2, 8.3
    """
    
    # Timeout for API calls
    API_TIMEOUT = 5.0
    
    def __init__(self, api_provider: str = "gemini", api_key: Optional[str] = None):
        """
        Initialize the image detector.
        
        Args:
            api_provider: Detection provider ('gemini' or 'yolo')
            api_key: API key for Gemini (required if using gemini)
            
        Raises:
            ValueError: If provider is not supported or API key missing
            
        Requirements: 8.2
        """
        self.api_provider = api_provider.lower()
        self.api_key = api_key or os.getenv('GEMINI_API_KEY', '')
        
        if self.api_provider not in ['gemini', 'yolo']:
            raise ValueError(
                f"Unsupported detection provider: {api_provider}. "
                "Supported providers: 'gemini', 'yolo'"
            )
        
        if self.api_provider == 'gemini' and not self.api_key:
            raise ValueError(
                "Gemini API key is required. "
                "Set GEMINI_API_KEY environment variable or pass api_key parameter."
            )
        
        # Configure API endpoint for Gemini
        if self.api_provider == 'gemini':
            self.api_url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-1.5-flash:generateContent?key={self.api_key}"
            )
    
    def detect_object(self, image_data: bytes, filename: str = "image") -> DetectionResult:
        """
        Detect objects in the provided image.
        
        Args:
            image_data: Image file data as bytes
            filename: Optional filename for context
            
        Returns:
            DetectionResult with primary object and confidence
            
        Raises:
            ValueError: If image is invalid or detection fails
            
        Requirements: 8.2, 8.3
        """
        # Validate image data
        try:
            image = Image.open(BytesIO(image_data))
            # Verify it's a valid image
            image.verify()
            # Reopen after verify (verify closes the file)
            image = Image.open(BytesIO(image_data))
        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")
        
        # Detect objects based on provider
        if self.api_provider == 'gemini':
            return self._detect_with_gemini(image_data)
        elif self.api_provider == 'yolo':
            return self._detect_with_yolo(image)
        
        raise ValueError(f"Detection provider {self.api_provider} not implemented")
    
    def _detect_with_gemini(self, image_data: bytes) -> DetectionResult:
        """
        Detect objects using Gemini Vision API.
        
        Args:
            image_data: Image file data as bytes
            
        Returns:
            DetectionResult with detected objects
            
        Raises:
            Exception: If API call fails
            
        Requirements: 8.2, 8.3
        """
        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Determine image MIME type
        image = Image.open(BytesIO(image_data))
        image_format = image.format.lower() if image.format else 'jpeg'
        mime_type = f"image/{image_format}"
        if mime_type == "image/jpg":
            mime_type = "image/jpeg"
        
        # Create prompt for object detection
        prompt = """Identify the main object in this image. 
Respond with ONLY the name of the primary object in the image as a single word (e.g., "apple", "car", "dog").
If there are multiple objects, choose the most prominent or central one.
Use simple, common English words suitable for pronunciation practice."""
        
        # Prepare API request
        headers = {'Content-Type': 'application/json'}
        payload = {
            'contents': [{
                'parts': [
                    {'text': prompt},
                    {
                        'inline_data': {
                            'mime_type': mime_type,
                            'data': image_base64
                        }
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.API_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract detected object from response
            if 'candidates' in data and len(data['candidates']) > 0:
                content = data['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    detected_text = content['parts'][0]['text'].strip()
                    
                    # Clean up the response - extract just the object name
                    # Remove any extra text, punctuation, or explanations
                    object_name = self._extract_object_name(detected_text)
                    
                    # Gemini doesn't provide confidence scores for vision tasks
                    # Use a default high confidence
                    confidence = 0.95
                    
                    return DetectionResult(
                        primary_object=object_name,
                        confidence=confidence,
                        all_objects=[(object_name, confidence)]
                    )
            
            raise ValueError("No object detected in image")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _extract_object_name(self, text: str) -> str:
        """
        Extract clean object name from API response text.
        
        Args:
            text: Raw text from API response
            
        Returns:
            Clean object name as single word
            
        Requirements: 8.3
        """
        # Remove common punctuation and extra whitespace
        text = text.strip().lower()
        
        # Remove quotes, periods, commas, etc.
        for char in ['"', "'", '.', ',', '!', '?', '\n', '\r']:
            text = text.replace(char, '')
        
        # Take first word if multiple words
        words = text.split()
        if words:
            # Filter out articles and common words
            filtered_words = [w for w in words if w not in ['the', 'a', 'an', 'is', 'it']]
            if filtered_words:
                return filtered_words[0]
            return words[0]
        
        return text
    
    def _detect_with_yolo(self, image: Image.Image) -> DetectionResult:
        """
        Detect objects using YOLO model.
        
        Note: This is a placeholder for YOLO integration.
        Requires additional dependencies (torch, ultralytics).
        
        Args:
            image: PIL Image object
            
        Returns:
            DetectionResult with detected objects
            
        Raises:
            NotImplementedError: YOLO integration not yet implemented
            
        Requirements: 8.2, 8.3
        """
        raise NotImplementedError(
            "YOLO detection not yet implemented. "
            "Use 'gemini' provider for object detection."
        )
    
    def get_primary_object(self, detections: List[Tuple[str, float]]) -> str:
        """
        Select the most prominent object from multiple detections.
        
        Args:
            detections: List of (object_name, confidence) tuples
            
        Returns:
            Name of the primary object
            
        Requirements: 8.3
        """
        if not detections:
            raise ValueError("No detections provided")
        
        # Sort by confidence (highest first)
        sorted_detections = sorted(detections, key=lambda x: x[1], reverse=True)
        
        # Return the object with highest confidence
        return sorted_detections[0][0]
