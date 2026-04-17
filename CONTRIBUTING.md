# Contributing to AI Pronunciation Coach

First off, thank you for considering contributing to AI Pronunciation Coach! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List some examples of how it would be used**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Ensure the test suite passes**
5. **Update documentation** as needed
6. **Write a clear commit message**

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest pytest-cov black flake8  # Dev dependencies
```

### Frontend Development

```bash
cd frontend
npm install
npm install --save-dev @types/node  # Dev dependencies
```

## Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

```python
def calculate_score(phoneme_comparison: PhonemeComparison) -> float:
    """
    Calculate pronunciation accuracy score.
    
    Args:
        phoneme_comparison: Comparison result of expected vs actual phonemes
        
    Returns:
        Accuracy score between 0.0 and 100.0
    """
    # Implementation
    pass
```

### TypeScript/React (Frontend)

- Use **TypeScript** for type safety
- Follow **React best practices**
- Use **functional components** with hooks
- Keep components **small and reusable**
- Use **meaningful component and variable names**

```typescript
interface AudioRecorderProps {
  onRecordingComplete: (blob: Blob) => void;
  maxDuration?: number;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ 
  onRecordingComplete,
  maxDuration = 5 
}) => {
  // Implementation
};
```

## Testing

### Backend Tests

```bash
cd backend
pytest app/modules/test_*.py -v
pytest --cov=app  # With coverage
```

### Writing Tests

- Write tests for **all new features**
- Aim for **high test coverage** (>80%)
- Use **descriptive test names**
- Test **edge cases** and **error conditions**

```python
def test_audio_input_accepts_valid_wav():
    """Test that valid WAV audio is accepted"""
    # Arrange
    audio_data = create_test_wav()
    
    # Act
    result = audio_input.accept_recording(audio_data, 'wav')
    
    # Assert
    assert result.is_valid
    assert result.audio_data is not None
```

## Commit Messages

Write clear, concise commit messages:

- Use the **present tense** ("Add feature" not "Added feature")
- Use the **imperative mood** ("Move cursor to..." not "Moves cursor to...")
- **Limit the first line** to 72 characters
- **Reference issues** and pull requests

Examples:
```
Add phoneme comparison visualization
Fix audio processing timeout issue
Update README with installation instructions
Refactor scoring engine for better performance
```

## Project Structure

### Adding New Backend Modules

1. Create module in `backend/app/modules/`
2. Add tests in `backend/app/modules/test_*.py`
3. Update `backend/main.py` if needed
4. Document in module README

### Adding New Frontend Components

1. Create component in `frontend/src/components/`
2. Add TypeScript types in `frontend/src/types/`
3. Update parent components as needed
4. Document component props

## Documentation

- Update **README.md** for major changes
- Add **inline comments** for complex logic
- Write **docstrings** for all public functions
- Update **API documentation** for endpoint changes

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Project README (for significant contributions)
- Release notes

Thank you for contributing! 🚀
