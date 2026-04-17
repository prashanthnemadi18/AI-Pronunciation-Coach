"""
Example usage of PhonemeAnalyzer module

Demonstrates how to use the phoneme analysis functionality for pronunciation evaluation.
"""

from phoneme_analyzer import PhonemeAnalyzer


def main():
    """Demonstrate PhonemeAnalyzer usage"""
    
    print("=" * 60)
    print("Phoneme Analyzer Example Usage")
    print("=" * 60)
    print()
    
    # Initialize analyzer
    print("1. Initializing PhonemeAnalyzer...")
    analyzer = PhonemeAnalyzer()
    print("   ✓ Analyzer initialized with CMU Dictionary")
    print()
    
    # Example 1: Perfect pronunciation
    print("2. Example 1: Perfect Pronunciation")
    print("-" * 60)
    target_word = "hello"
    transcribed_text = "hello"
    
    print(f"   Target word: '{target_word}'")
    print(f"   Transcribed: '{transcribed_text}'")
    print()
    
    # Get expected phonemes
    expected = analyzer.get_expected_phonemes(target_word)
    print(f"   Expected phonemes: {expected}")
    
    # Get actual phonemes
    actual = analyzer.get_actual_phonemes(transcribed_text)
    print(f"   Actual phonemes:   {actual}")
    print()
    
    # Compare phonemes
    result = analyzer.compare_phonemes(expected, actual)
    print(f"   Matches:       {len(result.matches)}/{len(expected)}")
    print(f"   Substitutions: {len(result.substitutions)}")
    print(f"   Missing:       {len(result.missing)}")
    print(f"   Extra:         {len(result.extra)}")
    print()
    
    # Example 2: Mispronunciation
    print("3. Example 2: Mispronunciation")
    print("-" * 60)
    target_word = "world"
    transcribed_text = "word"  # Missing 'l' sound
    
    print(f"   Target word: '{target_word}'")
    print(f"   Transcribed: '{transcribed_text}'")
    print()
    
    # Get expected phonemes
    expected = analyzer.get_expected_phonemes(target_word)
    print(f"   Expected phonemes: {expected}")
    
    # Get actual phonemes
    actual = analyzer.get_actual_phonemes(transcribed_text)
    print(f"   Actual phonemes:   {actual}")
    print()
    
    # Compare phonemes
    result = analyzer.compare_phonemes(expected, actual)
    print(f"   Matches:       {len(result.matches)}/{len(expected)}")
    print(f"   Substitutions: {len(result.substitutions)}")
    print(f"   Missing:       {len(result.missing)}")
    print(f"   Extra:         {len(result.extra)}")
    
    if result.substitutions:
        print(f"\n   Substitution details:")
        for idx, exp, act in result.substitutions:
            print(f"     Position {idx}: Expected '{exp}', got '{act}'")
    
    if result.missing:
        print(f"\n   Missing phonemes:")
        for idx, phoneme in result.missing:
            print(f"     Position {idx}: '{phoneme}'")
    
    if result.extra:
        print(f"\n   Extra phonemes:")
        for idx, phoneme in result.extra:
            print(f"     Position {idx}: '{phoneme}'")
    print()
    
    # Example 3: Phoneme substitution
    print("4. Example 3: Phoneme Substitution")
    print("-" * 60)
    target_word = "think"
    transcribed_text = "sink"  # TH -> S substitution
    
    print(f"   Target word: '{target_word}'")
    print(f"   Transcribed: '{transcribed_text}'")
    print()
    
    # Get expected phonemes
    expected = analyzer.get_expected_phonemes(target_word)
    print(f"   Expected phonemes: {expected}")
    
    # Get actual phonemes
    actual = analyzer.get_actual_phonemes(transcribed_text)
    print(f"   Actual phonemes:   {actual}")
    print()
    
    # Compare phonemes
    result = analyzer.compare_phonemes(expected, actual)
    print(f"   Matches:       {len(result.matches)}/{len(expected)}")
    print(f"   Substitutions: {len(result.substitutions)}")
    print(f"   Missing:       {len(result.missing)}")
    print(f"   Extra:         {len(result.extra)}")
    
    if result.substitutions:
        print(f"\n   Substitution details:")
        for idx, exp, act in result.substitutions:
            print(f"     Position {idx}: Expected '{exp}', got '{act}'")
    print()
    
    # Example 4: Cache demonstration
    print("5. Example 4: Cache Performance")
    print("-" * 60)
    import time
    
    word = "pronunciation"
    
    # First lookup (not cached)
    start = time.time()
    phonemes1 = analyzer.get_expected_phonemes(word)
    time1 = time.time() - start
    
    # Second lookup (cached)
    start = time.time()
    phonemes2 = analyzer.get_expected_phonemes(word)
    time2 = time.time() - start
    
    print(f"   Word: '{word}'")
    print(f"   Phonemes: {phonemes1}")
    print(f"   First lookup:  {time1*1000:.3f}ms")
    print(f"   Second lookup: {time2*1000:.3f}ms (cached)")
    print(f"   Speedup: {time1/time2:.1f}x faster")
    print()
    
    # Example 5: Multi-word transcription
    print("6. Example 5: Multi-word Transcription")
    print("-" * 60)
    target_word = "hello"
    transcribed_text = "hello world"  # Extra word
    
    print(f"   Target word: '{target_word}'")
    print(f"   Transcribed: '{transcribed_text}'")
    print()
    
    # Get expected phonemes
    expected = analyzer.get_expected_phonemes(target_word)
    print(f"   Expected phonemes: {expected}")
    
    # Get actual phonemes (includes both words)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    print(f"   Actual phonemes:   {actual}")
    print()
    
    # Compare phonemes
    result = analyzer.compare_phonemes(expected, actual)
    print(f"   Matches:       {len(result.matches)}/{len(expected)}")
    print(f"   Extra:         {len(result.extra)} (extra phonemes from 'world')")
    print()
    
    # Example 6: Error handling
    print("7. Example 6: Error Handling")
    print("-" * 60)
    
    try:
        invalid_word = "xyzabc123"
        print(f"   Attempting to get phonemes for: '{invalid_word}'")
        phonemes = analyzer.get_expected_phonemes(invalid_word)
    except ValueError as e:
        print(f"   ✓ Error caught: {e}")
    print()
    
    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
