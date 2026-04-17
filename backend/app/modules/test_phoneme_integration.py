"""
Integration tests for Phoneme Analyzer with other modules

Tests the complete flow from audio input through phoneme analysis.
"""

import pytest
from phoneme_analyzer import PhonemeAnalyzer


class TestPhonemeIntegration:
    """Integration tests for phoneme analysis pipeline"""
    
    @pytest.fixture
    def phoneme_analyzer(self):
        """Create PhonemeAnalyzer instance"""
        PhonemeAnalyzer.reset_instance()
        return PhonemeAnalyzer()
    
    def test_phoneme_analysis_pipeline(self, phoneme_analyzer):
        """Test phoneme analysis pipeline (simulating transcription result)"""
        
        # Simulate speech recognition output
        target_word = "hello"
        transcribed_text = "hello"
        
        # Step 1: Get expected phonemes
        expected = phoneme_analyzer.get_expected_phonemes(target_word)
        assert len(expected) > 0
        
        # Step 2: Get actual phonemes
        actual = phoneme_analyzer.get_actual_phonemes(transcribed_text)
        assert len(actual) > 0
        
        # Step 3: Compare phonemes
        comparison = phoneme_analyzer.compare_phonemes(expected, actual)
        
        assert comparison.expected_phonemes == expected
        assert comparison.actual_phonemes == actual
        assert len(comparison.matches) == len(expected)  # Perfect match
    
    def test_mispronunciation_detection(self, phoneme_analyzer):
        """Test detection of mispronunciation"""
        
        target_word = "think"
        transcribed_text = "sink"  # Common mispronunciation
        
        expected = phoneme_analyzer.get_expected_phonemes(target_word)
        actual = phoneme_analyzer.get_actual_phonemes(transcribed_text)
        
        comparison = phoneme_analyzer.compare_phonemes(expected, actual)
        
        # Should detect the TH -> S substitution
        assert len(comparison.substitutions) > 0 or len(comparison.matches) < len(expected)
    
    def test_multi_word_handling(self, phoneme_analyzer):
        """Test handling of multi-word transcriptions"""
        
        target_word = "hello"
        transcribed_text = "hello world"  # User said extra word
        
        expected = phoneme_analyzer.get_expected_phonemes(target_word)
        actual = phoneme_analyzer.get_actual_phonemes(transcribed_text)
        
        comparison = phoneme_analyzer.compare_phonemes(expected, actual)
        
        # Should have extra phonemes from "world"
        assert len(actual) > len(expected)
        assert len(comparison.extra) > 0
    
    def test_cache_performance_in_pipeline(self, phoneme_analyzer):
        """Test that caching improves performance in repeated lookups"""
        import time
        
        word = "pronunciation"
        
        # First lookup
        start = time.time()
        phonemes1 = phoneme_analyzer.get_expected_phonemes(word)
        time1 = time.time() - start
        
        # Second lookup (should be cached)
        start = time.time()
        phonemes2 = phoneme_analyzer.get_expected_phonemes(word)
        time2 = time.time() - start
        
        # Cached lookup should be faster
        assert time2 < time1
        assert phonemes1 == phonemes2
    
    def test_error_propagation(self, phoneme_analyzer):
        """Test that errors are properly propagated through pipeline"""
        
        # Test with invalid word
        with pytest.raises(ValueError) as exc_info:
            phoneme_analyzer.get_expected_phonemes("xyzabc123")
        
        assert "not found" in str(exc_info.value).lower()
        
        # Test with invalid transcription
        with pytest.raises(ValueError) as exc_info:
            phoneme_analyzer.get_actual_phonemes("xyzabc123")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_common_words_pronunciation(self, phoneme_analyzer):
        """Test phoneme analysis for common English words"""
        
        common_words = [
            ("hello", "hello"),
            ("world", "world"),
            ("test", "test"),
            ("python", "python"),
            ("computer", "computer"),
        ]
        
        for target, transcribed in common_words:
            expected = phoneme_analyzer.get_expected_phonemes(target)
            actual = phoneme_analyzer.get_actual_phonemes(transcribed)
            comparison = phoneme_analyzer.compare_phonemes(expected, actual)
            
            # Perfect pronunciation should have all matches
            assert len(comparison.matches) == len(expected)
            assert len(comparison.substitutions) == 0
            assert len(comparison.missing) == 0
            assert len(comparison.extra) == 0
    
    def test_phoneme_comparison_completeness(self, phoneme_analyzer):
        """Test that all phonemes are accounted for in comparison"""
        
        test_cases = [
            ("hello", "hello"),
            ("world", "word"),
            ("think", "sink"),
            ("cat", "cats"),
        ]
        
        for target, transcribed in test_cases:
            expected = phoneme_analyzer.get_expected_phonemes(target)
            actual = phoneme_analyzer.get_actual_phonemes(transcribed)
            comparison = phoneme_analyzer.compare_phonemes(expected, actual)
            
            # Every expected phoneme should be accounted for
            total_expected = (
                len(comparison.matches) +
                len(comparison.substitutions) +
                len(comparison.missing)
            )
            assert total_expected == len(expected), \
                f"Not all expected phonemes accounted for: {target} vs {transcribed}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
