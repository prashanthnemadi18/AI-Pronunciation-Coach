# Phoneme Analyzer Module

## Overview

The Phoneme Analyzer module extracts and compares phoneme sequences using the CMU Pronunciation Dictionary. It identifies matches, substitutions, missing, and extra phonemes for pronunciation evaluation.

## Features

- **Phoneme Extraction**: Convert words to phoneme sequences using CMU Dictionary
- **Phoneme Comparison**: Compare expected vs actual phoneme sequences
- **Error Detection**: Identify matches, substitutions, missing, and extra phonemes
- **Performance Optimization**: In-memory caching for phoneme lookups
- **Singleton Pattern**: Efficient dictionary loading and reuse
- **Error Handling**: Graceful handling of words not in dictionary

## Requirements Coverage

- **4.1**: Load CMU Pronunciation Dictionary
- **4.2**: Convert transcribed text to phoneme sequence
- **4.3**: Compare expected and actual phoneme sequences
- **4.4**: Identify matches and differences
- **4.5**: Handle words not found in dictionary
- **4.6**: Cache phoneme lookups for performance
- **4.7**: Pass comparison results to scoring engine

## Installation

```bash
pip install nltk==3.8.1
```

The CMU Dictionary will be automatically downloaded on first use.

## Usage

### Basic Usage

```python
from phoneme_analyzer import PhonemeAnalyzer

# Initialize analyzer (singleton pattern)
analyzer = PhonemeAnalyzer()

# Get expected phonemes for target word
target_word = "hello"
expected = analyzer.get_expected_phonemes(target_word)
print(f"Expected: {expected}")  # ['HH', 'AH', 'L', 'OW']

# Get actual phonemes from transcribed text
transcribed_text = "hello"
actual = analyzer.get_actual_phonemes(transcribed_text)
print(f"Actual: {actual}")  # ['HH', 'AH', 'L', 'OW']

# Compare phonemes
result = analyzer.compare_phonemes(expected, actual)
print(f"Matches: {len(result.matches)}/{len(expected)}")
print(f"Substitutions: {len(result.substitutions)}")
print(f"Missing: {len(result.missing)}")
print(f"Extra: {len(result.extra)}")
```

### Handling Mispronunciation

```python
# Example with mispronunciation
target_word = "think"
transcribed_text = "sink"  # TH -> S substitution

expected = analyzer.get_expected_phonemes(target_word)
actual = analyzer.get_actual_phonemes(transcribed_text)
result = analyzer.compare_phonemes(expected, actual)

# Check for substitutions
if result.substitutions:
    for idx, exp, act in result.substitutions:
        print(f"Position {idx}: Expected '{exp}', got '{act}'")
```

### Cache Usage

```python
# First lookup (loads from dictionary)
phonemes1 = analyzer.get_expected_phonemes("world")

# Check cache
cached = analyzer.cache_lookup("world")
if cached:
    print("Word found in cache!")

# Second lookup (uses cache - much faster)
phonemes2 = analyzer.get_expected_phonemes("world")
```

### Error Handling

```python
try:
    phonemes = analyzer.get_expected_phonemes("xyzabc123")
except ValueError as e:
    print(f"Error: {e}")
    # Error: Word 'xyzabc123' not found in CMU Pronunciation Dictionary
```

## Data Structures

### ComparisonResult

```python
@dataclass
class ComparisonResult:
    expected_phonemes: List[str]        # Expected phoneme sequence
    actual_phonemes: List[str]          # Actual phoneme sequence
    matches: List[Tuple[int, str]]      # (index, phoneme)
    substitutions: List[Tuple[int, str, str]]  # (index, expected, actual)
    missing: List[Tuple[int, str]]      # (index, expected phoneme)
    extra: List[Tuple[int, str]]        # (index, actual phoneme)
```

## API Reference

### PhonemeAnalyzer

#### `__init__(cmu_dict_path: Optional[str] = None)`

Initialize the phoneme analyzer with CMU Dictionary.

**Parameters:**
- `cmu_dict_path` (optional): Custom path to CMU dictionary file

**Raises:**
- `ImportError`: If nltk is not installed
- `RuntimeError`: If CMU dictionary cannot be loaded

#### `get_expected_phonemes(word: str) -> List[str]`

Retrieve expected phoneme sequence for a target word.

**Parameters:**
- `word`: Target word to get phonemes for

**Returns:**
- List of phoneme strings (e.g., `['HH', 'AH', 'L', 'OW']`)

**Raises:**
- `ValueError`: If word not found in dictionary

**Features:**
- Case-insensitive lookup
- Automatic caching
- Stress markers removed

#### `get_actual_phonemes(transcribed_text: str) -> List[str]`

Convert transcribed text to phoneme sequence.

**Parameters:**
- `transcribed_text`: Text from speech recognition

**Returns:**
- List of phoneme strings

**Raises:**
- `ValueError`: If text contains words not in dictionary

**Features:**
- Handles multiple words
- Removes punctuation
- Automatic caching

#### `compare_phonemes(expected: List[str], actual: List[str]) -> ComparisonResult`

Compare expected and actual phoneme sequences.

**Parameters:**
- `expected`: Expected phoneme sequence
- `actual`: Actual phoneme sequence

**Returns:**
- `ComparisonResult` with detailed comparison

**Algorithm:**
- Uses dynamic alignment to match phonemes
- Identifies matches, substitutions, missing, and extra phonemes
- Looks ahead to handle insertions/deletions

#### `cache_lookup(word: str) -> Optional[List[str]]`

Look up word in phoneme cache.

**Parameters:**
- `word`: Word to look up

**Returns:**
- Cached phoneme list or `None` if not in cache

## Phoneme Reference

The CMU Dictionary uses ARPAbet phoneme notation:

### Vowels
- **AA**: odd (AA D)
- **AE**: at (AE T)
- **AH**: hut (HH AH T)
- **AO**: ought (AO T)
- **AW**: cow (K AW)
- **AY**: hide (HH AY D)
- **EH**: Ed (EH D)
- **ER**: hurt (HH ER T)
- **EY**: ate (EY T)
- **IH**: it (IH T)
- **IY**: eat (IY T)
- **OW**: oat (OW T)
- **OY**: toy (T OY)
- **UH**: hood (HH UH D)
- **UW**: two (T UW)

### Consonants
- **B**: be (B IY)
- **CH**: cheese (CH IY Z)
- **D**: dee (D IY)
- **DH**: thee (DH IY)
- **F**: fee (F IY)
- **G**: green (G R IY N)
- **HH**: he (HH IY)
- **JH**: gee (JH IY)
- **K**: key (K IY)
- **L**: lee (L IY)
- **M**: me (M IY)
- **N**: knee (N IY)
- **NG**: ping (P IH NG)
- **P**: pee (P IY)
- **R**: read (R IY D)
- **S**: sea (S IY)
- **SH**: she (SH IY)
- **T**: tea (T IY)
- **TH**: theta (TH EY T AH)
- **V**: vee (V IY)
- **W**: we (W IY)
- **Y**: yield (Y IY L D)
- **Z**: zee (Z IY)
- **ZH**: seizure (S IY ZH ER)

## Performance

- **Dictionary Loading**: ~1-2 seconds on first initialization (singleton pattern)
- **First Lookup**: ~0.05ms per word
- **Cached Lookup**: ~0.003ms per word (15-20x faster)
- **Comparison**: O(n*m) where n, m are phoneme sequence lengths

## Testing

Run the test suite:

```bash
pytest test_phoneme_analyzer.py -v
```

Run the example usage:

```bash
python example_phoneme_analyzer_usage.py
```

## Integration with Other Modules

### Input from Speech Recognizer

```python
from speech_recognizer import SpeechRecognizer
from phoneme_analyzer import PhonemeAnalyzer

# Get transcription
recognizer = SpeechRecognizer()
transcription_result = recognizer.transcribe(audio_data)

# Analyze phonemes
analyzer = PhonemeAnalyzer()
target_word = "hello"
expected = analyzer.get_expected_phonemes(target_word)
actual = analyzer.get_actual_phonemes(transcription_result.transcribed_text)
comparison = analyzer.compare_phonemes(expected, actual)
```

### Output to Scoring Engine

```python
from phoneme_analyzer import PhonemeAnalyzer
from scoring_engine import ScoringEngine

# Get comparison result
analyzer = PhonemeAnalyzer()
comparison = analyzer.compare_phonemes(expected, actual)

# Calculate score
scorer = ScoringEngine()
score_result = scorer.calculate_score(comparison)
```

## Limitations

1. **Dictionary Coverage**: Only supports words in CMU Dictionary (~134,000 words)
2. **Single Pronunciation**: Uses first pronunciation variant for words with multiple
3. **English Only**: CMU Dictionary is English-specific
4. **No Stress Analysis**: Stress markers are removed from phonemes

## Future Enhancements

1. Support for multiple pronunciation variants
2. Custom dictionary additions
3. Stress pattern analysis
4. Multi-language support
5. Phoneme similarity scoring (e.g., TH vs S are similar)

## License

Part of the AI Pronunciation Coach system.
