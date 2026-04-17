"""
Example usage of the FeedbackGenerator module.

Demonstrates how to generate AI-powered pronunciation feedback using LLM APIs.
"""

import os
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine
from feedback_generator import FeedbackGenerator


def main():
    """Demonstrate feedback generator usage."""
    
    print("=== Feedback Generator Example Usage ===\n")
    
    # Initialize modules
    analyzer = PhonemeAnalyzer()
    scorer = ScoringEngine()
    
    # Get API key from environment (or use a test key)
    # For Gemini: export GEMINI_API_KEY=your_key
    # For Groq: export GROQ_API_KEY=your_key
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    groq_key = os.getenv('GROQ_API_KEY', '')
    
    # Choose provider based on available API key
    if gemini_key:
        print("Using Gemini API for feedback generation\n")
        feedback_gen = FeedbackGenerator('gemini', gemini_key)
    elif groq_key:
        print("Using Groq API for feedback generation\n")
        feedback_gen = FeedbackGenerator('groq', groq_key)
    else:
        print("No API key found. Demonstrating fallback feedback.\n")
        print("Set GEMINI_API_KEY or GROQ_API_KEY environment variable to use LLM.\n")
        # Use dummy key to trigger fallback
        feedback_gen = FeedbackGenerator('gemini', 'dummy_key')
    
    # Example 1: Perfect pronunciation
    print("Example 1: Perfect pronunciation of 'hello'")
    print("-" * 50)
    target_word = "hello"
    transcribed_text = "hello"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    score_result = scorer.calculate_score(comparison)
    feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Score: {score_result.accuracy_score:.1f}/100")
    print(f"\nCorrection tips: {feedback.correction_tips}")
    print(f"Encouragement: {feedback.encouragement}")
    print(f"Specific guidance: {feedback.specific_phoneme_guidance}")
    print()
    
    # Example 2: Pronunciation with errors
    print("Example 2: Mispronunciation of 'world' as 'word'")
    print("-" * 50)
    target_word = "world"
    transcribed_text = "word"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    score_result = scorer.calculate_score(comparison)
    feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Score: {score_result.accuracy_score:.1f}/100")
    print(f"\nCorrection tips: {feedback.correction_tips}")
    print(f"Encouragement: {feedback.encouragement}")
    print(f"\nSpecific phoneme guidance:")
    for phoneme, tip in feedback.specific_phoneme_guidance:
        print(f"  - {phoneme}: {tip}")
    print()
    
    # Example 3: Multiple errors
    print("Example 3: Wrong pronunciation of 'cat' as 'dog'")
    print("-" * 50)
    target_word = "cat"
    transcribed_text = "dog"
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    score_result = scorer.calculate_score(comparison)
    feedback = feedback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Expected phonemes: {expected}")
    print(f"Actual phonemes: {actual}")
    print(f"Score: {score_result.accuracy_score:.1f}/100")
    print(f"\nCorrection tips: {feedback.correction_tips}")
    print(f"Encouragement: {feedback.encouragement}")
    print(f"\nSpecific phoneme guidance:")
    for phoneme, tip in feedback.specific_phoneme_guidance:
        print(f"  - {phoneme}: {tip}")
    print()
    
    # Example 4: Demonstrating fallback feedback
    print("Example 4: Demonstrating fallback feedback mechanism")
    print("-" * 50)
    print("Creating feedback generator with invalid API key to trigger fallback...")
    fallback_gen = FeedbackGenerator('gemini', 'invalid_key_for_testing')
    
    target_word = "apple"
    transcribed_text = "apples"  # Extra 's'
    
    expected = analyzer.get_expected_phonemes(target_word)
    actual = analyzer.get_actual_phonemes(transcribed_text)
    comparison = analyzer.compare_phonemes(expected, actual)
    score_result = scorer.calculate_score(comparison)
    feedback = fallback_gen.generate_feedback(comparison, score_result.accuracy_score, target_word)
    
    print(f"Target word: {target_word}")
    print(f"Transcribed: {transcribed_text}")
    print(f"Score: {score_result.accuracy_score:.1f}/100")
    print(f"\nFallback correction tips: {feedback.correction_tips}")
    print(f"Fallback encouragement: {feedback.encouragement}")
    print()
    
    print("=== Feedback Generator Features ===")
    print("✓ Supports Gemini and Groq API providers")
    print("✓ Generates specific correction tips for mispronounced phonemes")
    print("✓ Provides encouraging feedback for correct pronunciation")
    print("✓ Implements fallback feedback for LLM API failures")
    print("✓ Completes feedback generation within 2 seconds")


if __name__ == "__main__":
    main()
