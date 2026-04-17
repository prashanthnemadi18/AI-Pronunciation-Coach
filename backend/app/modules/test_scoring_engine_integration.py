"""
Integration test for Scoring Engine module.

Tests the scoring engine with various phoneme comparison scenarios to verify
requirements are met.
"""

import time
from phoneme_analyzer import PhonemeAnalyzer, ComparisonResult
from scoring_engine import ScoringEngine


def test_score_range_invariant():
    """Test that scores are always between 0-100 (Requirement 5.1)"""
    print("Testing score range invariant...")
    
    scorer = ScoringEngine()
    
    # Test case 1: Perfect score
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C'],
        actual_phonemes=['A', 'B', 'C'],
        matches=[(0, 'A'), (1, 'B'), (2, 'C')],
        substitutions=[],
        missing=[],
        extra=[]
    )
    result = scorer.calculate_score(comparison)
    assert 0 <= result.accuracy_score <= 100, f"Score {result.accuracy_score} out of range"
    assert result.accuracy_score == 100.0, f"Perfect match should be 100, got {result.accuracy_score}"
    print(f"  ✓ Perfect match: {result.accuracy_score}")
    
    # Test case 2: Zero score (all wrong)
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C'],
        actual_phonemes=['X', 'Y', 'Z'],
        matches=[],
        substitutions=[(0, 'A', 'X'), (1, 'B', 'Y'), (2, 'C', 'Z')],
        missing=[],
        extra=[]
    )
    result = scorer.calculate_score(comparison)
    assert 0 <= result.accuracy_score <= 100, f"Score {result.accuracy_score} out of range"
    assert result.accuracy_score == 0.0, f"All wrong should be 0, got {result.accuracy_score}"
    print(f"  ✓ All wrong: {result.accuracy_score}")
    
    # Test case 3: Excessive penalties (should clamp to 0)
    comparison = ComparisonResult(
        expected_phonemes=['A'],
        actual_phonemes=['X', 'Y', 'Z', 'W'],
        matches=[],
        substitutions=[(0, 'A', 'X')],
        missing=[],
        extra=[(1, 'Y'), (2, 'Z'), (3, 'W')]
    )
    result = scorer.calculate_score(comparison)
    assert 0 <= result.accuracy_score <= 100, f"Score {result.accuracy_score} out of range"
    assert result.accuracy_score >= 0, f"Score should not be negative, got {result.accuracy_score}"
    print(f"  ✓ Excessive penalties clamped: {result.accuracy_score}")
    
    # Test case 4: Empty expected phonemes
    comparison = ComparisonResult(
        expected_phonemes=[],
        actual_phonemes=['A', 'B'],
        matches=[],
        substitutions=[],
        missing=[],
        extra=[(0, 'A'), (1, 'B')]
    )
    result = scorer.calculate_score(comparison)
    assert 0 <= result.accuracy_score <= 100, f"Score {result.accuracy_score} out of range"
    print(f"  ✓ Empty expected: {result.accuracy_score}")
    
    print("✓ Score range invariant test passed\n")


def test_penalty_weights():
    """Test that penalties are applied correctly (Requirements 5.2, 5.3)"""
    print("Testing penalty weights...")
    
    scorer = ScoringEngine()
    
    # Test substitution penalty
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C', 'D'],
        actual_phonemes=['A', 'X', 'C', 'D'],
        matches=[(0, 'A'), (2, 'C'), (3, 'D')],
        substitutions=[(1, 'B', 'X')],
        missing=[],
        extra=[]
    )
    result = scorer.calculate_score(comparison)
    expected_score = (100 * 3/4) - 10  # 75 - 10 = 65
    assert result.accuracy_score == expected_score, f"Expected {expected_score}, got {result.accuracy_score}"
    print(f"  ✓ Substitution penalty: {result.accuracy_score} (expected {expected_score})")
    
    # Test missing penalty
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C', 'D'],
        actual_phonemes=['A', 'C', 'D'],
        matches=[(0, 'A'), (2, 'C'), (3, 'D')],
        substitutions=[],
        missing=[(1, 'B')],
        extra=[]
    )
    result = scorer.calculate_score(comparison)
    expected_score = (100 * 3/4) - 15  # 75 - 15 = 60
    assert result.accuracy_score == expected_score, f"Expected {expected_score}, got {result.accuracy_score}"
    print(f"  ✓ Missing penalty: {result.accuracy_score} (expected {expected_score})")
    
    # Test extra penalty
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C'],
        actual_phonemes=['A', 'B', 'C', 'D'],
        matches=[(0, 'A'), (1, 'B'), (2, 'C')],
        substitutions=[],
        missing=[],
        extra=[(3, 'D')]
    )
    result = scorer.calculate_score(comparison)
    expected_score = 100 - 5  # 100 - 5 = 95
    assert result.accuracy_score == expected_score, f"Expected {expected_score}, got {result.accuracy_score}"
    print(f"  ✓ Extra penalty: {result.accuracy_score} (expected {expected_score})")
    
    # Test combined penalties
    comparison = ComparisonResult(
        expected_phonemes=['A', 'B', 'C', 'D'],
        actual_phonemes=['A', 'X', 'D', 'E'],
        matches=[(0, 'A'), (3, 'D')],
        substitutions=[(1, 'B', 'X')],
        missing=[(2, 'C')],
        extra=[(3, 'E')]
    )
    result = scorer.calculate_score(comparison)
    expected_score = (100 * 2/4) - 10 - 15 - 5  # 50 - 30 = 20
    assert result.accuracy_score == expected_score, f"Expected {expected_score}, got {result.accuracy_score}"
    print(f"  ✓ Combined penalties: {result.accuracy_score} (expected {expected_score})")
    
    print("✓ Penalty weights test passed\n")


def test_performance():
    """Test that scoring completes within 500ms (Requirement 5.5)"""
    print("Testing performance...")
    
    scorer = ScoringEngine()
    
    # Create a large comparison result
    expected = [f'P{i}' for i in range(100)]
    actual = [f'P{i}' for i in range(100)]
    matches = [(i, f'P{i}') for i in range(100)]
    
    comparison = ComparisonResult(
        expected_phonemes=expected,
        actual_phonemes=actual,
        matches=matches,
        substitutions=[],
        missing=[],
        extra=[]
    )
    
    # Measure time
    start_time = time.time()
    result = scorer.calculate_score(comparison)
    elapsed_time = time.time() - start_time
    
    print(f"  Scoring time: {elapsed_time*1000:.2f}ms")
    assert elapsed_time < 0.5, f"Scoring took {elapsed_time:.3f}s, exceeding 500ms limit"
    print("✓ Performance test passed\n")


def test_result_details():
    """Test that result includes all required details (Requirement 5.4)"""
    print("Testing result details...")
    
    scorer = ScoringEngine()
    analyzer = PhonemeAnalyzer()
    
    # Use real phoneme comparison
    expected = analyzer.get_expected_phonemes("world")
    actual = analyzer.get_actual_phonemes("word")
    comparison = analyzer.compare_phonemes(expected, actual)
    
    result = scorer.calculate_score(comparison)
    
    # Verify all fields are present
    assert hasattr(result, 'accuracy_score'), "Missing accuracy_score"
    assert hasattr(result, 'total_phonemes'), "Missing total_phonemes"
    assert hasattr(result, 'correct_phonemes'), "Missing correct_phonemes"
    assert hasattr(result, 'phoneme_details'), "Missing phoneme_details"
    
    # Verify values are correct
    assert result.total_phonemes == len(expected), "Incorrect total_phonemes"
    assert result.correct_phonemes == len(comparison.matches), "Incorrect correct_phonemes"
    assert result.phoneme_details == comparison, "Incorrect phoneme_details"
    
    print(f"  ✓ Accuracy score: {result.accuracy_score}")
    print(f"  ✓ Total phonemes: {result.total_phonemes}")
    print(f"  ✓ Correct phonemes: {result.correct_phonemes}")
    print(f"  ✓ Phoneme details: included")
    print("✓ Result details test passed\n")


def main():
    """Run all integration tests"""
    print("=== Scoring Engine Integration Tests ===\n")
    
    try:
        test_score_range_invariant()
        test_penalty_weights()
        test_performance()
        test_result_details()
        
        print("=" * 50)
        print("✓ ALL TESTS PASSED")
        print("=" * 50)
        print("\nRequirements verified:")
        print("  5.1: Score always between 0-100 ✓")
        print("  5.2: Matches weighted positively ✓")
        print("  5.3: Errors penalized correctly ✓")
        print("  5.4: Result includes all details ✓")
        print("  5.5: Scoring completes within 500ms ✓")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
