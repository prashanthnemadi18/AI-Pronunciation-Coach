# Scoring Engine Module

## Overview

The Scoring Engine module calculates pronunciation accuracy scores based on phoneme comparison results from the Phoneme Analyzer. It implements a weighted scoring algorithm that rewards correct phonemes and penalizes different types of errors.

## Requirements Coverage

- **5.1**: Calculate accuracy score between 0-100
- **5.2**: Weight phoneme matches positively
- **5.3**: Penalize substitutions, missing, and extra phonemes
- **5.4**: Return accuracy score with detailed phoneme-level results
- **5.5**: Complete scoring within 500 milliseconds

## Scoring Algorithm

The scoring algorithm uses the following formula:

```
Base Score = 100 × (matches / total_expected_phonemes)
Penalty = (substitutions × 10) + (missing × 15) + (extra × 5)
Final Score = max(0, min(100, Base Score - Penalty))
```

### Penalty Weights

- **Substitution**: -10 points (wrong phoneme used)
- **Missing**: -15 points (expected phoneme not pronounced)
- **Extra**: -5 points (additional phoneme pronounced)

The rationale:
- Missing phonemes are penalized most heavily as they represent omitted sounds
- Substitutions are moderately penalized as they represent incorrect sounds
- Extra phonemes are penalized least as they may be minor additions

## Usage

### Basic Usage

```python
from phoneme_analyzer import PhonemeAnalyzer, ComparisonResult
from scoring_engine import ScoringEngine

# Initialize modules
analyzer = PhonemeAnalyzer()
scorer = ScoringEngine()

# Get phoneme comparison
target_word = "hello"
transcribed_text = "hello"

expected = analyzer.get_expected_phonemes(target_word)
actual = analyzer.get_actual_phonemes(transcribed_text)
comparison = analyzer.compare_phonemes(expected, actual)

# Calculate score
result = scorer.calculate_score(comparison)

print(f"Accuracy: {result.accuracy_score:.1f}/100")
print(f"Correct: {result.correct_phonemes}/{result.total_phonemes}")
```

### Understanding the Results

The `ScoringResult` dataclass contains:

- `accuracy_score`: Float between 0-100 representing pronunciation accuracy
- `total_phonemes`: Total number of expected phonemes
- `correct_phonemes`: Number of correctly pronounced phonemes (matches)
- `phoneme_details`: Full ComparisonResult with detailed phoneme breakdown

## Examples

### Perfect Pronunciation

```python
# Target: "hello" → Transcribed: "hello"
# Expected: ['HH', 'AH', 'L', 'OW']
# Actual: ['HH', 'AH', 'L', 'OW']
# Score: 100.0 (4 matches, 0 errors)
```

### Partial Match with Substitution

```python
# Target: "hello" → Transcribed: "hallo"
# Expected: ['HH', 'AH', 'L', 'OW']
# Actual: ['HH', 'AE', 'L', 'OW']
# Score: 65.0 (3 matches, 1 substitution)
# Calculation: (100 × 3/4) - (1 × 10) = 75 - 10 = 65
```

### Missing Phonemes

```python
# Target: "world" → Transcribed: "word"
# Expected: ['W', 'ER', 'L', 'D']
# Actual: ['W', 'ER', 'D']
# Score: 60.0 (3 matches, 1 missing)
# Calculation: (100 × 3/4) - (1 × 15) = 75 - 15 = 60
```

### Extra Phonemes

```python
# Target: "cat" → Transcribed: "cats"
# Expected: ['K', 'AE', 'T']
# Actual: ['K', 'AE', 'T', 'S']
# Score: 95.0 (3 matches, 1 extra)
# Calculation: (100 × 3/3) - (1 × 5) = 100 - 5 = 95
```

### Multiple Errors

```python
# Target: "pronunciation" → Transcribed: "pronunshation"
# Multiple substitutions and errors
# Score calculated based on all error types
```

## Performance

The scoring engine is designed to complete calculations within 500ms as per requirement 5.5. The algorithm has O(1) complexity as it simply counts and applies penalties to pre-computed comparison results.

If scoring exceeds 500ms, a warning is logged but the operation completes normally.

## Integration with Pipeline

The Scoring Engine fits into the pronunciation evaluation pipeline:

```
Audio Input → Audio Processing → Speech Recognition
    ↓
Phoneme Analysis (comparison)
    ↓
Scoring Engine (calculate score) ← YOU ARE HERE
    ↓
Feedback Generation
```

## Testing

Run the example usage script:

```bash
cd backend/app/modules
python example_scoring_engine_usage.py
```

Run unit tests (when implemented):

```bash
pytest test_scoring_engine.py
```

## API Reference

### ScoringEngine Class

#### `__init__()`
Initialize the scoring engine.

#### `calculate_score(comparison: ComparisonResult) -> ScoringResult`
Calculate pronunciation accuracy score from phoneme comparison.

**Parameters:**
- `comparison`: ComparisonResult from PhonemeAnalyzer

**Returns:**
- `ScoringResult` with accuracy score and details

**Requirements:** 5.1, 5.2, 5.3, 5.4, 5.5

#### `weight_matches(matches: List[Tuple[int, str]]) -> float`
Calculate positive weight contribution from phoneme matches.

**Parameters:**
- `matches`: List of matched phonemes

**Returns:**
- Weighted score contribution

**Requirements:** 5.2

#### `penalize_errors(substitutions, missing, extra) -> float`
Calculate penalty from pronunciation errors.

**Parameters:**
- `substitutions`: List of substituted phonemes
- `missing`: List of missing phonemes
- `extra`: List of extra phonemes

**Returns:**
- Total penalty value

**Requirements:** 5.3

### ScoringResult Dataclass

```python
@dataclass
class ScoringResult:
    accuracy_score: float      # 0-100
    total_phonemes: int        # Total expected phonemes
    correct_phonemes: int      # Number of matches
    phoneme_details: ComparisonResult  # Full comparison details
```

## Error Handling

The scoring engine handles edge cases:

- **Empty expected phonemes**: Returns score of 0.0
- **No actual phonemes**: All expected phonemes marked as missing
- **Score out of bounds**: Automatically clamped to [0, 100]

## Dependencies

- `phoneme_analyzer.ComparisonResult`: Input data structure
- `dataclasses`: For ScoringResult
- `typing`: Type hints
- `time`: Performance monitoring

## Future Enhancements

Potential improvements for future versions:

1. Configurable penalty weights
2. Phoneme-specific penalties (some sounds harder than others)
3. Position-based weighting (errors at start vs. end)
4. Confidence scores from speech recognition
5. Language-specific scoring adjustments
