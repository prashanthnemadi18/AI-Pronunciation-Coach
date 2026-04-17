"""
Example usage of the ImageDetector module.

Demonstrates how to detect objects in images for pronunciation practice.
"""

import os
from image_detector import ImageDetector


def main():
    """Demonstrate image detector usage."""
    
    print("=== Image Detector Example Usage ===\n")
    
    # Get API key from environment
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    
    if not gemini_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Please set it to use the image detector:")
        print("  export GEMINI_API_KEY=your_api_key")
        print("\nYou can get a Gemini API key from:")
        print("  https://makersuite.google.com/app/apikey")
        return
    
    # Initialize image detector
    print("Initializing ImageDetector with Gemini Vision API...\n")
    detector = ImageDetector(api_provider='gemini', api_key=gemini_key)
    
    # Example: Detect object in a sample image
    # Note: In real usage, you would load an actual image file
    print("Example: Detecting objects in images")
    print("-" * 50)
    print("\nTo use this example, you need to provide an image file.")
    print("Here's how to use the ImageDetector:\n")
    
    print("# Load image from file")
    print("with open('path/to/image.jpg', 'rb') as f:")
    print("    image_data = f.read()")
    print()
    print("# Detect object in image")
    print("result = detector.detect_object(image_data, filename='image.jpg')")
    print()
    print("# Access detection results")
    print("print(f'Primary object: {result.primary_object}')")
    print("print(f'Confidence: {result.confidence:.2f}')")
    print("print(f'All objects: {result.all_objects}')")
    print()
    
    # Demonstrate get_primary_object method
    print("\nExample: Selecting primary object from multiple detections")
    print("-" * 50)
    
    # Simulate multiple detections
    detections = [
        ("apple", 0.95),
        ("banana", 0.87),
        ("orange", 0.72)
    ]
    
    primary = detector.get_primary_object(detections)
    print(f"Detections: {detections}")
    print(f"Primary object (highest confidence): {primary}")
    print()
    
    # Show error handling
    print("\nExample: Error handling")
    print("-" * 50)
    print("The ImageDetector handles various error cases:")
    print("✓ Invalid image data (corrupted files)")
    print("✓ Unsupported image formats")
    print("✓ API failures with descriptive error messages")
    print("✓ Empty detection results")
    print()
    
    print("=== Image Detector Features ===")
    print("✓ Detects objects using Gemini Vision API")
    print("✓ Returns primary object name for pronunciation practice")
    print("✓ Handles multiple objects by selecting most prominent")
    print("✓ Validates image data before processing")
    print("✓ Provides confidence scores for detections")
    print("✓ Supports common image formats (JPEG, PNG, etc.)")
    print()
    
    print("=== Integration with Pronunciation Coach ===")
    print("1. User uploads an image in Image Mode")
    print("2. ImageDetector identifies the primary object")
    print("3. Object name becomes the target word")
    print("4. User pronounces the word")
    print("5. System evaluates pronunciation as in Audio Mode")


if __name__ == "__main__":
    main()
