"""
Scoring Engine Module

Calculates pronunciation accuracy scores based on phoneme comparison results.
Weights matches positively and penalizes substitutions, missing, and extra phonemes.
"""

from dataclasses import dataclass
from typing import List, Tuple
import time


# Import ComparisonResult from phoneme_analyzer
try:
    from .phoneme_analyzer import ComparisonResult
except ImportError:
    from phoneme_analyzer import ComparisonResult


@dataclass
class ScoringResult:
    """Result of pronunciation scoring"""
    accuracy_score: float  # 0-100
    total_phonemes: int
    correct_phonemes: int
    phoneme_details: ComparisonResult


class ScoringEngine:
    """
    Calculates pronunciation accuracy scores from phoneme comparison results.
    
    Scoring Algorithm:
    - Base score: 100 * (matches / total_expected_phonemes)
    - Penalty for substitutions: -10 per substitution
    - Penalty for missing phonemes: -15 per missing
    - Penalty for extra phonemes: -5 per extra
    - Final score clamped to [0, 100]
    
    Requirements Coverage: 5.1, 5.2, 5.3, 5.4, 5.5
    """
    
    # Penalty weights for different error types
    SUBSTITUTION_PENALTY = 10
    MISSING_PENALTY = 15
    EXTRA_PENALTY = 5
    
    def __init__(self):
        """
        Initialize the scoring engine.
        
        Requirements: 5.1
        """
        pass
    
    def calculate_score(self, comparison: ComparisonResult) -> ScoringResult:
        """
        Calculate pronunciation accuracy score from phoneme comparison.
        
        Args:
            comparison: ComparisonResult from PhonemeAnalyzer
            
        Returns:
            ScoringResult with accuracy score and details
            
        Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
        """
        start_time = time.time()
        
        # Get counts of each error type
        num_matches = len(comparison.matches)
        num_substitutions = len(comparison.substitutions)
        num_missing = len(comparison.missing)
        num_extra = len(comparison.extra)
        
        # Total expected phonemes
        total_expected = len(comparison.expected_phonemes)
        
        # Handle edge case: no expected phonemes
        if total_expected == 0:
            score = 0.0
        else:
            # Calculate base score from matches (Requirement 5.2)
            base_score = 100.0 * (num_matches / total_expected)
            
            # Apply penalties (Requirement 5.3)
            penalty = (
                num_substitutions * self.SUBSTITUTION_PENALTY +
                num_missing * self.MISSING_PENALTY +
                num_extra * self.EXTRA_PENALTY
            )
            
            # Calculate final score
            score = base_score - penalty
            
            # Clamp score to [0, 100] range (Requirement 5.1)
            score = max(0.0, min(100.0, score))
        
        # Ensure scoring completes within 500ms (Requirement 5.5)
        elapsed_time = time.time() - start_time
        if elapsed_time > 0.5:
            # Log warning but don't fail
            print(f"Warning: Scoring took {elapsed_time:.3f}s, exceeding 500ms target")
        
        return ScoringResult(
            accuracy_score=score,
            total_phonemes=total_expected,
            correct_phonemes=num_matches,
            phoneme_details=comparison
        )
    
    def weight_matches(self, matches: List[Tuple[int, str]]) -> float:
        """
        Calculate positive weight contribution from phoneme matches.
        
        Args:
            matches: List of matched phonemes from comparison
            
        Returns:
            Weighted score contribution from matches
            
        Requirements: 5.2
        """
        # Each match contributes equally to the base score
        # This is already handled in calculate_score via the base_score calculation
        return float(len(matches))
    
    def penalize_errors(
        self,
        substitutions: List[Tuple[int, str, str]],
        missing: List[Tuple[int, str]],
        extra: List[Tuple[int, str]]
    ) -> float:
        """
        Calculate penalty from pronunciation errors.
        
        Args:
            substitutions: List of substituted phonemes
            missing: List of missing phonemes
            extra: List of extra phonemes
            
        Returns:
            Total penalty value
            
        Requirements: 5.3
        """
        penalty = (
            len(substitutions) * self.SUBSTITUTION_PENALTY +
            len(missing) * self.MISSING_PENALTY +
            len(extra) * self.EXTRA_PENALTY
        )
        return penalty
