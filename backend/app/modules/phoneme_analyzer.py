"""
Phoneme Analysis Module

Extracts and compares phoneme sequences using the CMU Pronunciation Dictionary.
Identifies matches, substitutions, missing, and extra phonemes for pronunciation evaluation.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import threading

try:
    import nltk
    from nltk.corpus import cmudict
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


@dataclass
class ComparisonResult:
    """Result of phoneme comparison"""
    expected_phonemes: List[str]
    actual_phonemes: List[str]
    matches: List[Tuple[int, str]]  # (index, phoneme)
    substitutions: List[Tuple[int, str, str]]  # (index, expected, actual)
    missing: List[Tuple[int, str]]  # (index, expected phoneme)
    extra: List[Tuple[int, str]]  # (index, actual phoneme)


class PhonemeAnalyzer:
    """
    Handles phoneme extraction and comparison using CMU Pronunciation Dictionary.
    
    Implements in-memory caching for performance optimization.
    
    Requirements Coverage: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
    """
    
    _instance = None
    _lock = threading.Lock()
    _cmu_dict = None
    _phoneme_cache: Dict[str, List[str]] = {}
    
    def __new__(cls, cmu_dict_path: Optional[str] = None):
        """
        Implement singleton pattern for dictionary loading.
        
        Requirements: 4.6 (performance optimization)
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, cmu_dict_path: Optional[str] = None):
        """
        Initialize the phoneme analyzer with CMU Dictionary.
        
        Args:
            cmu_dict_path: Optional path to CMU dictionary file (uses NLTK's by default)
            
        Requirements: 4.1
        """
        if not NLTK_AVAILABLE:
            raise ImportError(
                "nltk is required for phoneme analysis. "
                "Install it with: pip install nltk"
            )
        
        # Only load dictionary if not already loaded
        if self._cmu_dict is None:
            with self._lock:
                if self._cmu_dict is None:
                    self._load_cmu_dictionary(cmu_dict_path)
    
    def _load_cmu_dictionary(self, cmu_dict_path: Optional[str] = None):
        """
        Load CMU Pronunciation Dictionary.
        
        Args:
            cmu_dict_path: Optional custom path to dictionary
            
        Requirements: 4.1
        """
        try:
            # Download CMU dictionary if not already present
            try:
                nltk.data.find('corpora/cmudict')
            except LookupError:
                nltk.download('cmudict', quiet=True)
            
            # Load the dictionary
            self._cmu_dict = cmudict.dict()
            
        except Exception as e:
            raise RuntimeError(f"Failed to load CMU Pronunciation Dictionary: {str(e)}")
    
    def get_expected_phonemes(self, word: str) -> List[str]:
        """
        Retrieve expected phoneme sequence for a target word from CMU Dictionary.
        
        Args:
            word: Target word to get phonemes for
            
        Returns:
            List of phoneme strings
            
        Raises:
            ValueError: If word not found in dictionary
            
        Requirements: 4.1, 4.5, 4.6
        """
        # Normalize word to lowercase
        word_lower = word.lower().strip()
        
        # Check cache first (Requirement 4.6)
        if word_lower in self._phoneme_cache:
            return self._phoneme_cache[word_lower]
        
        # Look up in CMU dictionary
        if word_lower not in self._cmu_dict:
            raise ValueError(
                f"Word '{word}' not found in CMU Pronunciation Dictionary. "
                "This word is not currently supported."
            )
        
        # Get phoneme list (CMU dict may have multiple pronunciations, use first)
        phoneme_list = self._cmu_dict[word_lower][0]
        
        # Remove stress markers (0, 1, 2) from phonemes
        phonemes = [self._remove_stress(p) for p in phoneme_list]
        
        # Cache the result (Requirement 4.6)
        self._phoneme_cache[word_lower] = phonemes
        
        return phonemes
    
    def get_actual_phonemes(self, transcribed_text: str) -> List[str]:
        """
        Convert transcribed text to phoneme sequence.
        
        Args:
            transcribed_text: Text from speech recognition
            
        Returns:
            List of phoneme strings
            
        Raises:
            ValueError: If text contains words not in dictionary
            
        Requirements: 4.2, 4.5
        """
        # Normalize and split text into words
        words = transcribed_text.lower().strip().split()
        
        if not words:
            return []
        
        # Get phonemes for each word
        all_phonemes = []
        for word in words:
            # Remove punctuation
            word_clean = ''.join(c for c in word if c.isalnum())
            
            if not word_clean:
                continue
            
            # Check cache first
            if word_clean in self._phoneme_cache:
                phonemes = self._phoneme_cache[word_clean]
            else:
                # Look up in dictionary
                if word_clean not in self._cmu_dict:
                    raise ValueError(
                        f"Word '{word_clean}' not found in CMU Pronunciation Dictionary"
                    )
                
                phoneme_list = self._cmu_dict[word_clean][0]
                phonemes = [self._remove_stress(p) for p in phoneme_list]
                
                # Cache the result
                self._phoneme_cache[word_clean] = phonemes
            
            all_phonemes.extend(phonemes)
        
        return all_phonemes
    
    def compare_phonemes(
        self, 
        expected: List[str], 
        actual: List[str]
    ) -> ComparisonResult:
        """
        Compare expected and actual phoneme sequences.
        
        Identifies:
        - Matches: phonemes that are correct
        - Substitutions: phonemes that are wrong
        - Missing: expected phonemes not present in actual
        - Extra: actual phonemes not in expected
        
        Args:
            expected: Expected phoneme sequence
            actual: Actual phoneme sequence from transcription
            
        Returns:
            ComparisonResult with detailed comparison
            
        Requirements: 4.3, 4.4, 4.7
        """
        matches: List[Tuple[int, str]] = []
        substitutions: List[Tuple[int, str, str]] = []
        missing: List[Tuple[int, str]] = []
        extra: List[Tuple[int, str]] = []
        
        # Use dynamic programming approach (similar to edit distance)
        # to find optimal alignment between expected and actual phonemes
        
        len_expected = len(expected)
        len_actual = len(actual)
        
        # Simple alignment: iterate through both sequences
        i = 0  # index in expected
        j = 0  # index in actual
        
        while i < len_expected or j < len_actual:
            if i >= len_expected:
                # Remaining actual phonemes are extra
                extra.append((j, actual[j]))
                j += 1
            elif j >= len_actual:
                # Remaining expected phonemes are missing
                missing.append((i, expected[i]))
                i += 1
            elif expected[i] == actual[j]:
                # Match found
                matches.append((i, expected[i]))
                i += 1
                j += 1
            else:
                # Check if it's a substitution or insertion/deletion
                # Look ahead to see if we can find a match
                found_match = False
                
                # Look ahead in actual for expected[i]
                for k in range(j + 1, min(j + 3, len_actual)):
                    if expected[i] == actual[k]:
                        # Found match ahead, mark current as extra
                        extra.append((j, actual[j]))
                        j += 1
                        found_match = True
                        break
                
                if not found_match:
                    # Look ahead in expected for actual[j]
                    for k in range(i + 1, min(i + 3, len_expected)):
                        if expected[k] == actual[j]:
                            # Found match ahead, mark current as missing
                            missing.append((i, expected[i]))
                            i += 1
                            found_match = True
                            break
                
                if not found_match:
                    # No match found nearby, treat as substitution
                    substitutions.append((i, expected[i], actual[j]))
                    i += 1
                    j += 1
        
        return ComparisonResult(
            expected_phonemes=expected,
            actual_phonemes=actual,
            matches=matches,
            substitutions=substitutions,
            missing=missing,
            extra=extra
        )
    
    def cache_lookup(self, word: str) -> Optional[List[str]]:
        """
        Look up word in phoneme cache.
        
        Args:
            word: Word to look up
            
        Returns:
            Cached phoneme list or None if not in cache
            
        Requirements: 4.6
        """
        word_lower = word.lower().strip()
        return self._phoneme_cache.get(word_lower)
    
    def _remove_stress(self, phoneme: str) -> str:
        """
        Remove stress markers (0, 1, 2) from phoneme.
        
        Args:
            phoneme: Phoneme string possibly with stress marker
            
        Returns:
            Phoneme without stress marker
        """
        # CMU dict phonemes may end with 0, 1, or 2 for stress
        return ''.join(c for c in phoneme if not c.isdigit())
    
    @classmethod
    def reset_instance(cls):
        """
        Reset singleton instance (useful for testing).
        """
        with cls._lock:
            cls._instance = None
            cls._cmu_dict = None
            cls._phoneme_cache = {}
