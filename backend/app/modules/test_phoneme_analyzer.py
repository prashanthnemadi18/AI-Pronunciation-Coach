"""
Unit tests for Phoneme Analysis Module

Tests phoneme extraction, comparison, and caching functionality.
"""

import pytest
from phoneme_analyzer import PhonemeAnalyzer, ComparisonResult


class TestPhonemeAnalyzer:
    """Test suite for PhonemeAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create PhonemeAnalyzer instance for testing"""
        # Reset singleton to ensure clean state
        PhonemeAnalyzer.reset_instance()
        return PhonemeAnalyzer()
    
    def test_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer is not None
        assert analyzer._cmu_dict is not None
    
    def test_singleton_pattern(self):
        """Test that PhonemeAnalyzer follows singleton pattern"""
        PhonemeAnalyzer.reset_instance()
        analyzer1 = PhonemeAnalyzer()
        analyzer2 = PhonemeAnalyzer()
        assert analyzer1 is analyzer2
    
    def test_get_expected_phonemes_simple_word(self, analyzer):
        """Test getting phonemes for a simple word"""
        phonemes = analyzer.get_expected_phonemes("hello")
        assert isinstance(phonemes, list)
        assert len(phonemes) > 0
        # "hello" should have phonemes like ['HH', 'AH', 'L', 'OW'] or similar
        assert all(isinstance(p, str) for p in phonemes)
    
    def test_get_expected_phonemes_caching(self, analyzer):
        """Test that phoneme lookups are cached"""
        word = "world"
        
        # First lookup
        phonemes1 = analyzer.get_expected_phonemes(word)
        
        # Check cache
        cached = analyzer.cache_lookup(word)
        assert cached is not None
        assert cached == phonemes1
        
        # Second lookup should return same result
        phonemes2 = analyzer.get_expected_phonemes(word)
        assert phonemes1 == phonemes2
    
    def test_get_expected_phonemes_word_not_found(self, analyzer):
        """Test error handling for words not in dictionary"""
        with pytest.raises(ValueError) as exc_info:
            analyzer.get_expected_phonemes("xyzabc123")
        assert "not found" in str(exc_info.value).lower()
    
    def test_get_expected_phonemes_case_insensitive(self, analyzer):
        """Test that word lookup is case-insensitive"""
        phonemes_lower = analyzer.get_expected_phonemes("hello")
        phonemes_upper = analyzer.get_expected_phonemes("HELLO")
        phonemes_mixed = analyzer.get_expected_phonemes("HeLLo")
        
        assert phonemes_lower == phonemes_upper == phonemes_mixed
    
    def test_get_actual_phonemes_single_word(self, analyzer):
        """Test converting transcribed text to phonemes"""
        phonemes = analyzer.get_actual_phonemes("hello")
        assert isinstance(phonemes, list)
        assert len(phonemes) > 0
    
    def test_get_actual_phonemes_multiple_words(self, analyzer):
        """Test converting multi-word text to phonemes"""
        phonemes = analyzer.get_actual_phonemes("hello world")
        assert isinstance(phonemes, list)
        # Should have phonemes from both words
        assert len(phonemes) > 5
    
    def test_get_actual_phonemes_empty_text(self, analyzer):
        """Test handling of empty text"""
        phonemes = analyzer.get_actual_phonemes("")
        assert phonemes == []
    
    def test_get_actual_phonemes_with_punctuation(self, analyzer):
        """Test that punctuation is handled correctly"""
        phonemes = analyzer.get_actual_phonemes("hello!")
        assert isinstance(phonemes, list)
        assert len(phonemes) > 0
    
    def test_compare_phonemes_perfect_match(self, analyzer):
        """Test comparison with perfect pronunciation"""
        expected = ["HH", "AH", "L", "OW"]
        actual = ["HH", "AH", "L", "OW"]
        
        result = analyzer.compare_phonemes(expected, actual)
        
        assert isinstance(result, ComparisonResult)
        assert len(result.matches) == 4
        assert len(result.substitutions) == 0
        assert len(result.missing) == 0
        assert len(result.extra) == 0
    
    def test_compare_phonemes_with_substitution(self, analyzer):
        """Test comparison with phoneme substitution"""
        expected = ["HH", "AH", "L", "OW"]
        actual = ["HH", "EH", "L", "OW"]  # AH -> EH substitution
        
        result = analyzer.compare_phonemes(expected, actual)
        
        assert len(result.matches) == 3  # HH, L, OW match
        assert len(result.substitutions) == 1
        assert result.substitutions[0][1] == "AH"  # expected
        assert result.substitutions[0][2] == "EH"  # actual
    
    def test_compare_phonemes_with_missing(self, analyzer):
        """Test comparison with missing phonemes"""
        expected = ["HH", "AH", "L", "OW"]
        actual = ["HH", "L", "OW"]  # Missing AH
        
        result = analyzer.compare_phonemes(expected, actual)
        
        assert len(result.missing) >= 1
        # Should identify that AH is missing
    
    def test_compare_phonemes_with_extra(self, analyzer):
        """Test comparison with extra phonemes"""
        expected = ["HH", "AH", "L", "OW"]
        actual = ["HH", "AH", "R", "L", "OW"]  # Extra R
        
        result = analyzer.compare_phonemes(expected, actual)
        
        assert len(result.extra) >= 1
        # Should identify extra phoneme
    
    def test_compare_phonemes_empty_sequences(self, analyzer):
        """Test comparison with empty sequences"""
        result = analyzer.compare_phonemes([], [])
        
        assert len(result.matches) == 0
        assert len(result.substitutions) == 0
        assert len(result.missing) == 0
        assert len(result.extra) == 0
    
    def test_compare_phonemes_completeness(self, analyzer):
        """Test that all phonemes are accounted for in comparison"""
        expected = ["HH", "AH", "L", "OW"]
        actual = ["HH", "EH", "L"]
        
        result = analyzer.compare_phonemes(expected, actual)
        
        # Every expected phoneme should be either matched, substituted, or missing
        total_expected_accounted = (
            len(result.matches) + 
            len(result.substitutions) + 
            len(result.missing)
        )
        assert total_expected_accounted == len(expected)
    
    def test_end_to_end_pronunciation_evaluation(self, analyzer):
        """Test complete flow: target word -> expected -> actual -> compare"""
        target_word = "hello"
        transcribed_text = "hello"
        
        # Get expected phonemes
        expected = analyzer.get_expected_phonemes(target_word)
        
        # Get actual phonemes
        actual = analyzer.get_actual_phonemes(transcribed_text)
        
        # Compare
        result = analyzer.compare_phonemes(expected, actual)
        
        # Should be perfect match
        assert len(result.matches) == len(expected)
        assert len(result.substitutions) == 0
        assert len(result.missing) == 0
        assert len(result.extra) == 0
    
    def test_end_to_end_mispronunciation(self, analyzer):
        """Test complete flow with mispronunciation"""
        target_word = "hello"
        transcribed_text = "halo"  # Mispronounced
        
        # Get expected phonemes
        expected = analyzer.get_expected_phonemes(target_word)
        
        # Get actual phonemes
        actual = analyzer.get_actual_phonemes(transcribed_text)
        
        # Compare
        result = analyzer.compare_phonemes(expected, actual)
        
        # Should have some differences
        assert len(result.matches) < len(expected) or len(result.substitutions) > 0
    
    def test_cache_lookup_existing_word(self, analyzer):
        """Test cache lookup for existing word"""
        word = "test"
        
        # First get phonemes to populate cache
        phonemes = analyzer.get_expected_phonemes(word)
        
        # Lookup in cache
        cached = analyzer.cache_lookup(word)
        
        assert cached is not None
        assert cached == phonemes
    
    def test_cache_lookup_nonexistent_word(self, analyzer):
        """Test cache lookup for word not in cache"""
        cached = analyzer.cache_lookup("nonexistentword123")
        assert cached is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
