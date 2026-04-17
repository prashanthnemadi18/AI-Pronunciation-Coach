"""
Integration test for FeedbackGenerator module.

Tests the complete flow: PhonemeAnalyzer → ScoringEngine → FeedbackGenerator
"""

import pytest
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine
from feedback_generator import FeedbackGenerator


class TestFeedbackIntegration:
    """Integration tests for feedback generation pipeline."""
    
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
        """Create FeedbackGenerator instance with dummy key (will use fallback)."""
        return FeedbackGenerator('gemini', 'test_key')
    
    def test_perfect_pronunciation_feedback(self, analyzer, scorer, feedback_gen):
        """Test feedback generation for perfect pronunciation."""
        target_word = "hello"
        transcribed_text = "hello"
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results
        assert score_result.accuracy_score == 100.0
        assert "perfect" in feedback.correction_tips.lower() or "no corrections" in feedback.correction_tips.lower()
        assert len(feedback.specific_phoneme_guidance) == 0
        assert len(feedback.encouragement) > 0
    
    def test_mispronunciation_feedback(self, analyzer, scorer, feedback_gen):
        """Test feedback generation for mispronunciation."""
        target_word = "world"
        transcribed_text = "word"
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results
        assert score_result.accuracy_score < 100.0
        assert len(feedback.correction_tips) > 0
        assert len(feedback.encouragement) > 0
        # Should have guidance since there are errors
        assert "L" in feedback.correction_tips or len(feedback.specific_phoneme_guidance) > 0
    
    def test_multiple_errors_feedback(self, analyzer, scorer, feedback_gen):
        """Test feedback generation for multiple pronunciation errors."""
        target_word = "cat"
        transcribed_text = "dog"
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results
        assert score_result.accuracy_score < 50.0  # Should be low score
        assert len(feedback.correction_tips) > 0
        assert len(feedback.specific_phoneme_guidance) > 0  # Should have multiple tips
        assert len(feedback.encouragement) > 0
    
    def test_extra_phonemes_feedback(self, analyzer, scorer, feedback_gen):
        """Test feedback generation for extra phonemes."""
        target_word = "apple"
        transcribed_text = "apples"
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify results
        assert score_result.accuracy_score > 80.0  # Should be high but not perfect
        assert len(feedback.correction_tips) > 0
        assert "extra" in feedback.correction_tips.lower() or len(comparison.extra) > 0
    
    def test_feedback_structure(self, analyzer, scorer, feedback_gen):
        """Test that feedback has correct structure."""
        target_word = "test"
        transcribed_text = "best"
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify structure
        assert hasattr(feedback, 'correction_tips')
        assert hasattr(feedback, 'encouragement')
        assert hasattr(feedback, 'specific_phoneme_guidance')
        assert isinstance(feedback.correction_tips, str)
        assert isinstance(feedback.encouragement, str)
        assert isinstance(feedback.specific_phoneme_guidance, list)
    
    def test_invalid_provider(self):
        """Test that invalid provider raises error."""
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            FeedbackGenerator('invalid_provider', 'test_key')
    
    def test_fallback_always_works(self, analyzer, scorer):
        """Test that fallback feedback always works even with invalid API key."""
        feedback_gen = FeedbackGenerator('gemini', 'definitely_invalid_key')
        
        target_word = "hello"
        transcribed_text = "yellow"  # Different word but valid
        
        # Process through pipeline
        expected = analyzer.get_expected_phonemes(target_word)
        actual = analyzer.get_actual_phonemes(transcribed_text)
        comparison = analyzer.compare_phonemes(expected, actual)
        score_result = scorer.calculate_score(comparison)
        
        # Should not raise exception, should use fallback
        feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
        
        # Verify fallback feedback is provided
        assert len(feedback.correction_tips) > 0
        assert len(feedback.encouragement) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
