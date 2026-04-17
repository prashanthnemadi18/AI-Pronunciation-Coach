"""
Feedback Generation Module

Generates AI-powered pronunciation correction tips using LLM (Gemini or Groq).
Provides specific guidance on mispronounced phonemes and encouraging feedback.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import time
import requests
import os


# Import ComparisonResult from phoneme_analyzer
try:
    from .phoneme_analyzer import ComparisonResult
except ImportError:
    from phoneme_analyzer import ComparisonResult


@dataclass
class FeedbackResult:
    """Result of feedback generation"""
    correction_tips: str
    encouragement: str
    specific_phoneme_guidance: List[Tuple[str, str]]  # (phoneme, tip)


class FeedbackGenerator:
    """
    Generates AI-powered pronunciation feedback using LLM APIs.
    
    Supports Gemini and Groq API providers for generating personalized
    correction tips based on phoneme-level analysis.
    
    Requirements Coverage: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6
    """
    
    # Timeout for LLM API calls (2 seconds as per requirement 6.5)
    API_TIMEOUT = 2.0
    
    def __init__(self, llm_provider: str, api_key: str):
        """
        Initialize the feedback generator with LLM provider.
        
        Args:
            llm_provider: LLM provider name ('gemini' or 'groq')
            api_key: API key for the LLM provider
            
        Raises:
            ValueError: If provider is not supported
            
        Requirements: 6.2
        """
        self.llm_provider = llm_provider.lower()
        self.api_key = api_key
        
        if self.llm_provider not in ['gemini', 'groq']:
            raise ValueError(
                f"Unsupported LLM provider: {llm_provider}. "
                "Supported providers: 'gemini', 'groq'"
            )
        
        # Configure API endpoints
        if self.llm_provider == 'gemini':
            self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        elif self.llm_provider == 'groq':
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def generate_feedback(
        self,
        comparison: ComparisonResult,
        score: float,
        target_word: str = ""
    ) -> FeedbackResult:
        """
        Generate pronunciation feedback based on phoneme comparison.
        
        Args:
            comparison: ComparisonResult from PhonemeAnalyzer
            score: Accuracy score from ScoringEngine
            target_word: Optional target word for context
            
        Returns:
            FeedbackResult with correction tips and encouragement
            
        Requirements: 6.1, 6.3, 6.4, 6.5, 6.6
        """
        start_time = time.time()
        
        # Check if pronunciation is perfect (Requirement 6.4)
        if len(comparison.substitutions) == 0 and \
           len(comparison.missing) == 0 and \
           len(comparison.extra) == 0:
            return self._generate_perfect_feedback(score)
        
        # Try to generate feedback using LLM (Requirement 6.1, 6.2)
        try:
            prompt = self._create_prompt(comparison, score, target_word)
            feedback_text = self._call_llm_api(prompt)
            
            # Parse feedback into structured format
            result = self._parse_feedback(feedback_text, comparison)
            
            # Ensure completion within 2 seconds (Requirement 6.5)
            elapsed_time = time.time() - start_time
            if elapsed_time > self.API_TIMEOUT:
                print(f"Warning: Feedback generation took {elapsed_time:.3f}s, exceeding 2s target")
            
            return result
            
        except Exception as e:
            # Fallback to generic feedback if LLM fails (Requirement 6.6)
            print(f"LLM API error: {str(e)}. Using fallback feedback.")
            return self._get_fallback_feedback(comparison, score)
    
    def _create_prompt(
        self,
        comparison: ComparisonResult,
        score: float,
        target_word: str
    ) -> str:
        """
        Create prompt for LLM to generate feedback.
        
        Args:
            comparison: ComparisonResult with phoneme details
            score: Accuracy score
            target_word: Target word being pronounced
            
        Returns:
            Formatted prompt string
            
        Requirements: 6.3
        """
        # Build error details
        error_details = []
        
        if comparison.substitutions:
            subs = [f"{exp} → {act}" for _, exp, act in comparison.substitutions]
            error_details.append(f"Substitutions: {', '.join(subs)}")
        
        if comparison.missing:
            miss = [phoneme for _, phoneme in comparison.missing]
            error_details.append(f"Missing phonemes: {', '.join(miss)}")
        
        if comparison.extra:
            ext = [phoneme for _, phoneme in comparison.extra]
            error_details.append(f"Extra phonemes: {', '.join(ext)}")
        
        error_text = "; ".join(error_details)
        
        prompt = f"""You are a pronunciation coach helping a student improve their pronunciation.

The student attempted to pronounce the word "{target_word}".
Expected phonemes: {' '.join(comparison.expected_phonemes)}
Actual phonemes: {' '.join(comparison.actual_phonemes)}
Accuracy score: {score:.1f}/100

Errors identified: {error_text}

Provide specific, actionable tips to improve pronunciation. Focus on:
1. How to correctly pronounce the incorrect phonemes
2. Mouth position and tongue placement
3. Encouraging words to motivate the student

Keep your response concise (2-3 sentences) and friendly."""
        
        return prompt
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call LLM API to generate feedback.
        
        Args:
            prompt: Formatted prompt for LLM
            
        Returns:
            Generated feedback text
            
        Raises:
            Exception: If API call fails
            
        Requirements: 6.2, 6.5
        """
        headers = {}
        payload = {}
        
        if self.llm_provider == 'gemini':
            headers = {'Content-Type': 'application/json'}
            payload = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }]
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.API_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            feedback_text = data['candidates'][0]['content']['parts'][0]['text']
            
        elif self.llm_provider == 'groq':
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'model': 'mixtral-8x7b-32768',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 200
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.API_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            feedback_text = data['choices'][0]['message']['content']
        
        return feedback_text.strip()
    
    def _parse_feedback(
        self,
        feedback_text: str,
        comparison: ComparisonResult
    ) -> FeedbackResult:
        """
        Parse LLM feedback into structured format.
        
        Args:
            feedback_text: Raw feedback from LLM
            comparison: ComparisonResult for extracting phoneme guidance
            
        Returns:
            Structured FeedbackResult
            
        Requirements: 6.3
        """
        # Extract specific phoneme guidance from errors
        specific_guidance = []
        
        for _, expected, actual in comparison.substitutions:
            tip = f"Replace '{actual}' sound with '{expected}' sound"
            specific_guidance.append((expected, tip))
        
        for _, phoneme in comparison.missing:
            tip = f"Don't forget to pronounce the '{phoneme}' sound"
            specific_guidance.append((phoneme, tip))
        
        # Split feedback into correction tips and encouragement
        # Simple heuristic: last sentence is encouragement if it contains positive words
        sentences = feedback_text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        encouragement = "Keep practicing, you're making progress!"
        correction_tips = feedback_text
        
        if sentences:
            last_sentence = sentences[-1].lower()
            positive_words = ['great', 'good', 'well', 'keep', 'progress', 'improve', 'better']
            
            if any(word in last_sentence for word in positive_words):
                encouragement = sentences[-1] + "."
                correction_tips = '. '.join(sentences[:-1]) + "."
        
        return FeedbackResult(
            correction_tips=correction_tips,
            encouragement=encouragement,
            specific_phoneme_guidance=specific_guidance
        )
    
    def _generate_perfect_feedback(self, score: float) -> FeedbackResult:
        """
        Generate encouraging feedback for perfect pronunciation.
        
        Args:
            score: Accuracy score (should be high)
            
        Returns:
            FeedbackResult with encouragement
            
        Requirements: 6.4
        """
        encouragement_messages = [
            "Perfect pronunciation! Excellent work!",
            "Outstanding! You nailed it!",
            "Flawless pronunciation! Keep it up!",
            "Brilliant! Your pronunciation is spot on!",
            "Excellent job! You've mastered this word!"
        ]
        
        # Select encouragement based on score
        import random
        encouragement = random.choice(encouragement_messages)
        
        return FeedbackResult(
            correction_tips="No corrections needed - your pronunciation is perfect!",
            encouragement=encouragement,
            specific_phoneme_guidance=[]
        )
    
    def _get_fallback_feedback(
        self,
        comparison: ComparisonResult,
        score: float
    ) -> FeedbackResult:
        """
        Generate generic fallback feedback when LLM is unavailable.
        
        Args:
            comparison: ComparisonResult with phoneme details
            score: Accuracy score
            
        Returns:
            FeedbackResult with generic tips
            
        Requirements: 6.6
        """
        # Build generic correction tips
        tips = []
        
        if comparison.substitutions:
            for _, expected, actual in comparison.substitutions:
                tips.append(f"Try pronouncing '{expected}' instead of '{actual}'")
        
        if comparison.missing:
            missing_phonemes = [phoneme for _, phoneme in comparison.missing]
            tips.append(f"Don't forget to pronounce: {', '.join(missing_phonemes)}")
        
        if comparison.extra:
            extra_phonemes = [phoneme for _, phoneme in comparison.extra]
            tips.append(f"Avoid adding extra sounds: {', '.join(extra_phonemes)}")
        
        correction_tips = ". ".join(tips) + "." if tips else "Focus on matching the expected phoneme sequence."
        
        # Generic encouragement based on score
        if score >= 80:
            encouragement = "You're very close! Keep practicing."
        elif score >= 60:
            encouragement = "Good effort! A bit more practice will help."
        else:
            encouragement = "Keep trying! Practice makes perfect."
        
        # Build specific phoneme guidance
        specific_guidance = []
        for _, expected, actual in comparison.substitutions:
            tip = f"Replace '{actual}' with '{expected}'"
            specific_guidance.append((expected, tip))
        
        return FeedbackResult(
            correction_tips=correction_tips,
            encouragement=encouragement,
            specific_phoneme_guidance=specific_guidance
        )
