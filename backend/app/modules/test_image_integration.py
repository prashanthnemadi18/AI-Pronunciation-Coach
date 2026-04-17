"""
Integration test for ImageDetector module with pronunciation pipeline.

Tests the complete flow: ImageDetector → PhonemeAnalyzer → ScoringEngine → FeedbackGenerator
"""

import pytest
from io import BytesIO
from PIL import Image
from image_detector import ImageDetector, DetectionResult
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine
from feedback_generator import FeedbackGenerator


class TestImageDetectorIntegration:
    """Integration tests for image detection with pronunciation pipeline."""
    
    @pytest.fixture
    def detector(self):
        """Create ImageDetector instance."""
        return ImageDetector(api_provider='gemini', api_key='test_key')
    
    @pytest.fixture
    def analyzer(self):
        """Create PhonemeAnalyzer instance."""
        return PhonemeAnalyzer()
    
    @pytest.fixture
    def scorer(self):
        """Create ScoringEngine instance."""
        return ScoringEngine()
    
    @pytest.fixture
    def feedback_gen(self):
        """Create FeedbackGenerator instance."""
        return FeedbackGenerator('gemini', 'test_key')
    
    def test_image_mode_workflow_simulation(self, detector, analyzer, scorer, feedback_gen):
        """
        Simulate the complete Image Mode workflow.
        
        Workflow:
        1. User uploads image
        2. System detects object (simulated)
        3. Object name becomes target word
        4. User pronounces word (simulated)
        5. System evaluates pronunciation
        """
        # Step 1 & 2: Simulate object detection
        # In real scenario, this would be: detector.detect_object(image_data)
        # For testing, we simulate the detection result
        simulated_detection = DetectionResult(
            primary_object="apple",
            confidence=0.95,
            all_objects=[("apple", 0.95)]
        )
        
        target_word = simulated_detection.primary_object
        assert target_word == "apple"
        
        # Step 3: User sees prompt to pronounce "apple"
        print(f"\nPlease pronounce: {target_word}")
        
        # Step 4: Simulate user pronunciation (transcribed as "apple")
        transcribed_text = "apple"
        
        # Step 5: Evaluate pronunciation through standard pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results
        assert score_result.accuracy_score == 100.0
        assert len(feedback.correction_tips) > 0
        assert len(feedback.encouragement) > 0
        print(f"Score: {score_result.accuracy_score:.1f}/100")
        print(f"Feedback: {feedback.encouragement}")
    
    def test_image_mode_with_mispronunciation(self, detector, analyzer, scorer, feedback_gen):
        """Test Image Mode workflow with mispronunciation."""
        # Simulate detection
        simulated_detection = DetectionResult(
            primary_object="cat",
            confidence=0.92,
            all_objects=[("cat", 0.92)]
        )
        
        target_word = simulated_detection.primary_object
        
        # Simulate mispronunciation
        transcribed_text = "bat"  # User said "bat" instead of "cat"
        
        # Evaluate pronunciation
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results show error
        assert score_result.accuracy_score < 100.0
        assert len(comparison.substitutions) > 0 or len(comparison.missing) > 0
        assert len(feedback.specific_phoneme_guidance) > 0
    
    def test_primary_object_selection_integration(self, detector, analyzer, scorer):
        """Test selecting primary object from multiple detections."""
        # Simulate multiple objects detected
        detections = [
            ("banana", 0.87),
            ("apple", 0.95),  # Highest confidence
            ("orange", 0.72)
        ]
        
        # Select primary object
        target_word = detector.get_primary_object(detections)
        assert target_word == "apple"
        
        # Verify it can be used in pronunciation pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        assert len(expected) > 0
        
        # Simulate perfect pronunciation
        actual = analyzer.get_actual_phonemes(target_word)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        
        assert score_result.accuracy_score == 100.0
    
    def test_detection_result_to_pronunciation_pipeline(self, analyzer, scorer, feedback_gen):
        """Test that DetectionResult integrates smoothly with pronunciation pipeline."""
        # Create detection result
        detection = DetectionResult(
            primary_object="dog",
            confidence=0.98,
            all_objects=[("dog", 0.98), ("puppy", 0.65)]
        )
        
        # Use primary object as target word
        target_word = detection.primary_object
        
        # Simulate pronunciation
        transcribed_text = "dog"
        
        # Run through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify complete flow works
        assert isinstance(score_result.accuracy_score, float)
        assert 0 <= score_result.accuracy_score <= 100
        assert isinstance(feedback.correction_tips, str)
        assert isinstance(feedback.encouragement, str)
    
    def test_image_mode_error_handling(self, detector):
        """Test error handling in Image Mode workflow."""
        # Test invalid image data
        invalid_data = b"not an image"
        
        with pytest.raises(ValueError, match="Invalid image data"):
            detector.detect_object(invalid_data)
    
    def test_confidence_threshold_concept(self, detector):
        """Test concept of confidence-based object selection."""
        # Simulate low confidence detections
        low_confidence_detections = [
            ("unclear_object", 0.45),
            ("maybe_something", 0.38)
        ]
        
        # System should still select highest confidence
        primary = detector.get_primary_object(low_confidence_detections)
        assert primary == "unclear_object"
        
        # In production, you might want to add a confidence threshold
        # and reject detections below a certain confidence level


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
