"""
Example usage of the ScoringEngine module.

Demonstrates how to calculate pronunciation accuracy scores from phoneme comparison results.
"""

from phoneme_analyzer import PhonemeAnalyzer, ComparisonResult
from scoring_engine import ScoringEngine


def main():
    """Demonstrate scoring engine usage."""
    
    # Initialize modules
    analyzer = PhonemeAnalyzer()
    scorer = ScoringEngine()
    
    print("=== Scoring Engine Example Usage ===\n")
    
    # Example 1: Perfect pronunciation
    print("Example 1: Perfect pronunciation of 'hello'")
    target_word = "hello"
    transcribed_text = "hello"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    result = scorer.calculate_score(comparison)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Accuracy score: {result.accuracy_score:.1f}/100")
    print(f"Correct phonemes: {result.correct_phonemes}/{result.total_phonemes}")
    print()
    
    # Example 2: Pronunciation with errors
    print("Example 2: Mispronunciation of 'world' as 'word'")
    target_word = "world"
    transcribed_text = "word"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    result = scorer.calculate_score(comparison)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Matches: {len(comparison.matches)}")
    print(f"Substitutions: {len(comparison.substitutions)}")
    print(f"Missing: {len(comparison.missing)}")
    print(f"Extra: {len(comparison.extra)}")
    print(f"Accuracy score: {result.accuracy_score:.1f}/100")
    print(f"Correct phonemes: {result.correct_phonemes}/{result.total_phonemes}")
    print()
    
    # Example 3: Completely wrong pronunciation
    print("Example 3: Wrong pronunciation of 'cat' as 'dog'")
    target_word = "cat"
    transcribed_text = "dog"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    result = scorer.calculate_score(comparison)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Matches: {len(comparison.matches)}")
    print(f"Substitutions: {len(comparison.substitutions)}")
    print(f"Missing: {len(comparison.missing)}")
    print(f"Extra: {len(comparison.extra)}")
    print(f"Accuracy score: {result.accuracy_score:.1f}/100")
    print(f"Correct phonemes: {result.correct_phonemes}/{result.total_phonemes}")
    print()
    
    # Example 4: Partial match with extra phonemes
    print("Example 4: 'apple' pronounced as 'apples'")
    target_word = "apple"
    transcribed_text = "apples"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    result = scorer.calculate_score(comparison)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Matches: {len(comparison.matches)}")
    print(f"Substitutions: {len(comparison.substitutions)}")
    print(f"Missing: {len(comparison.missing)}")
    print(f"Extra: {len(comparison.extra)}")
    print(f"Accuracy score: {result.accuracy_score:.1f}/100")
    print(f"Correct phonemes: {result.correct_phonemes}/{result.total_phonemes}")
    print()
    
    # Example 5: Demonstrate penalty calculation
    print("Example 5: Understanding penalty weights")
    print(f"Substitution penalty: {scorer.SUBSTITUTION_PENALTY} points")
    print(f"Missing phoneme penalty: {scorer.MISSING_PENALTY} points")
    print(f"Extra phoneme penalty: {scorer.EXTRA_PENALTY} points")
    print()
    print("Scoring formula:")
    print("  Base score = 100 * (matches / total_expected)")
    print("  Penalty = (substitutions * 10) + (missing * 15) + (extra * 5)")
    print("  Final score = max(0, min(100, base_score - penalty))")


if __name__ == "__main__":
    main()
