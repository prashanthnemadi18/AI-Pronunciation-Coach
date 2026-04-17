# Feedback Generator Module

## Overview

The Feedback Generator module generates AI-powered pronunciation correction tips using LLM APIs (Gemini or Groq). It provides specific guidance on mispronounced phonemes and encouraging feedback to help users improve their pronunciation.

## Features

- **LLM Integration**: Supports both Gemini and Groq API providers
- **Specific Correction Tips**: Generates actionable tips for mispronounced phonemes
- **Encouraging Feedback**: Provides motivational messages based on performance
- **Fallback Mechanism**: Returns generic feedback when LLM API is unavailable
- **Performance**: Completes feedback generation within 2 seconds

## Requirements Coverage

- **6.1**: Generates correction tips when phoneme comparison indicates errors
- **6.2**: Uses Gemini or Groq API for generating feedback
- **6.3**: Provides specific guidance on how to correct mispronounced phonemes
- **6.4**: Returns encouraging feedback when all phonemes are correct
- **6.5**: Completes feedback generation within 2 seconds
- **6.6**: Returns generic fallback feedback when LLM API is unavailable

## Installation

The module requires the `requests` library for API calls:

```bash
pip install requests
```

## Usage

### Basic Usage

```python
from feedback_generator import FeedbackGenerator
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine

# Initialize modules
analyzer = PhonemeAnalyzer()
scorer = ScoringEngine()
feedback_gen = FeedbackGenerator('gemini', 'your_api_key')

# Analyze pronunciation
target_word = "hello"
transcribed_text = "helo"

expected = analyzer.get_expected_phonemes(target_word)
actual = analyzer.get_actual_phonemes(transcribed_text)
comparison = analyzer.compare_phonemes(expected, actual)
score_result = scorer.calculate_score(comparison)

# Generate feedback
feedback = feedback_gen.generate_feedback(
    comparison, 
    score_result.accuracy_score, 
    target_word
)

print(f"Correction tips: {feedback.correction_tips}")
print(f"Encouragement: {feedback.encouragement}")
```

### Using Gemini API

```python
import os

gemini_key = os.getenv('GEMINI_API_KEY')
feedback_gen = FeedbackGenerator('gemini', gemini_key)

feedback = feedback_gen.generate_feedback(comparison, score, target_word)
```

### Using Groq API

```python
import os

groq_key = os.getenv('GROQ_API_KEY')
feedback_gen = FeedbackGenerator('groq', groq_key)

feedback = feedback_gen.generate_feedback(comparison, score, target_word)
```

### Handling API Failures

The module automatically falls back to generic feedback when the LLM API is unavailable:

```python
# Even if API fails, you'll still get useful feedback
try:
    feedback = feedback_gen.generate_feedback(comparison, score, target_word)
    # feedback.correction_tips will contain either LLM-generated or fallback tips
except Exception as e:
    print(f"Error: {e}")
```

## API Configuration

### Gemini API

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable: `export GEMINI_API_KEY=your_key`
3. Initialize: `FeedbackGenerator('gemini', api_key)`

### Groq API

1. Get API key from [Groq Console](https://console.groq.com/)
2. Set environment variable: `export GROQ_API_KEY=your_key`
3. Initialize: `FeedbackGenerator('groq', api_key)`

## Data Structures

### FeedbackResult

```python
@dataclass
class FeedbackResult:
    correction_tips: str                              # Main correction advice
    encouragement: str                                # Motivational message
    specific_phoneme_guidance: List[Tuple[str, str]]  # [(phoneme, tip), ...]
```

## Example Output

### Perfect Pronunciation

```
Correction tips: No corrections needed - your pronunciation is perfect!
Encouragement: Perfect pronunciation! Excellent work!
Specific guidance: []
```

### With Errors

```
Correction tips: Try pronouncing 'L' instead of 'W'. Focus on placing your tongue behind your upper teeth for the 'L' sound.
Encouragement: You're very close! Keep practicing.
Specific guidance: [('L', "Replace 'W' sound with 'L' sound")]
```

### Fallback Feedback

```
Correction tips: Try pronouncing 'AH' instead of 'EH'. Don't forget to pronounce: L.
Encouragement: Good effort! A bit more practice will help.
Specific guidance: [('AH', "Replace 'EH' with 'AH'")]
```

## Performance

- **API Timeout**: 2 seconds (as per requirement 6.5)
- **Fallback**: Instant (no API call)
- **Warning**: Logs warning if generation exceeds 2 seconds

## Error Handling

The module handles various error scenarios:

1. **Invalid API Key**: Falls back to generic feedback
2. **Network Timeout**: Falls back to generic feedback after 2 seconds
3. **API Rate Limiting**: Falls back to generic feedback
4. **Invalid Provider**: Raises `ValueError` during initialization

## Testing

Run the example usage script:

```bash
cd backend/app/modules
python example_feedback_generator_usage.py
```

Set API keys to test LLM integration:

```bash
export GEMINI_API_KEY=your_key
python example_feedback_generator_usage.py
```

## Integration with Other Modules

The Feedback Generator integrates with:

1. **PhonemeAnalyzer**: Receives `ComparisonResult` with phoneme details
2. **ScoringEngine**: Receives accuracy score for context
3. **API Endpoints**: Used in `/api/pronunciation/evaluate` endpoint

## Prompt Engineering

The module constructs prompts that include:

- Target word
- Expected vs. actual phonemes
- Accuracy score
- Specific error details (substitutions, missing, extra)
- Instructions for concise, actionable feedback

## Future Enhancements

- Support for additional LLM providers (OpenAI, Anthropic)
- Caching of feedback for common error patterns
- Multi-language support
- Personalized feedback based on user history
- Audio pronunciation examples via TTS

## Troubleshooting

### No API Key

```
Error: Unsupported LLM provider
Solution: Ensure you're using 'gemini' or 'groq' as provider name
```

### Timeout Issues

```
Warning: Feedback generation took 2.5s, exceeding 2s target
Solution: Module automatically falls back to generic feedback
```

### API Errors

```
LLM API error: 401 Unauthorized. Using fallback feedback.
Solution: Check your API key is valid and has sufficient quota
```

## License

Part of the AI Pronunciation Coach project.
