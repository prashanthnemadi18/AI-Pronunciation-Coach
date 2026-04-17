# Requirements Document

## Introduction

The AI Pronunciation Coach is a system that evaluates user pronunciation accuracy through phoneme-level analysis and provides real-time feedback. The system accepts audio input (recorded or uploaded), processes it through speech recognition, compares phoneme sequences against expected pronunciations, calculates accuracy scores, and generates AI-powered correction tips. The system supports three interaction modes: Audio Mode for direct pronunciation practice, Image Mode for object-based pronunciation challenges, and Game Mode for gamified learning with scoring and timers.

## Glossary

- **Audio_Input_Module**: Component that captures or receives audio data from the user
- **Audio_Processor**: Component that cleans and normalizes raw audio data
- **Speech_Recognizer**: Component that converts speech audio to text transcription using Whisper
- **Phoneme_Analyzer**: Component that converts text to phoneme sequences and compares them
- **CMU_Dictionary**: Carnegie Mellon University pronunciation dictionary mapping words to phonemes
- **Scoring_Engine**: Component that calculates pronunciation accuracy scores
- **Feedback_Generator**: Component that generates correction tips using LLM
- **Pronunciation_Attempt**: A single user attempt to pronounce a word or phrase
- **Phoneme**: The smallest unit of sound in speech
- **Target_Word**: The word the user is attempting to pronounce
- **Accuracy_Score**: Numerical representation of pronunciation correctness (0-100)
- **Frontend_Client**: React-based user interface application
- **Backend_API**: FastAPI-based server handling requests
- **User_Session**: A period of interaction by a single user
- **Practice_Mode**: One of three interaction modes (Audio, Image, or Game)

## Requirements

### Requirement 1: Audio Input Capture

**User Story:** As a user, I want to record my voice or upload audio files, so that I can have my pronunciation evaluated.

#### Acceptance Criteria

1. THE Audio_Input_Module SHALL accept audio recordings from the user's microphone
2. THE Audio_Input_Module SHALL accept uploaded audio files in WAV, MP3, or M4A formats
3. WHEN audio duration exceeds 5 seconds, THE Audio_Input_Module SHALL reject the input and return an error message
4. WHEN audio is captured, THE Audio_Input_Module SHALL pass the audio data to the Audio_Processor
5. THE Audio_Input_Module SHALL provide visual feedback indicating recording status

### Requirement 2: Audio Processing

**User Story:** As a developer, I want audio to be cleaned and normalized, so that speech recognition accuracy is improved.

#### Acceptance Criteria

1. WHEN raw audio is received, THE Audio_Processor SHALL normalize the audio volume
2. THE Audio_Processor SHALL remove background noise from the audio
3. THE Audio_Processor SHALL convert audio to a format compatible with the Speech_Recognizer
4. WHEN audio processing fails, THE Audio_Processor SHALL return a descriptive error message
5. THE Audio_Processor SHALL complete processing within 2 seconds for audio up to 5 seconds in length

### Requirement 3: Speech-to-Text Conversion

**User Story:** As a user, I want my speech converted to text, so that the system can analyze what I said.

#### Acceptance Criteria

1. WHEN processed audio is received, THE Speech_Recognizer SHALL transcribe the audio to text using Whisper
2. THE Speech_Recognizer SHALL use a small or base Whisper model for performance optimization
3. WHEN transcription produces no text, THE Speech_Recognizer SHALL return an error indicating no speech detected
4. THE Speech_Recognizer SHALL pass the transcribed text to the Phoneme_Analyzer
5. THE Speech_Recognizer SHALL complete transcription within 3 seconds for audio up to 5 seconds in length

### Requirement 4: Phoneme Extraction and Comparison

**User Story:** As a user, I want my pronunciation compared at the phoneme level, so that I receive accurate feedback on specific sound errors.

#### Acceptance Criteria

1. WHEN a Target_Word is provided, THE Phoneme_Analyzer SHALL retrieve the expected phoneme sequence from the CMU_Dictionary
2. WHEN transcribed text is received, THE Phoneme_Analyzer SHALL convert it to an actual phoneme sequence
3. THE Phoneme_Analyzer SHALL compare the expected phoneme sequence with the actual phoneme sequence
4. THE Phoneme_Analyzer SHALL identify which phonemes match and which differ
5. WHEN a Target_Word is not found in the CMU_Dictionary, THE Phoneme_Analyzer SHALL return an error message
6. THE Phoneme_Analyzer SHALL cache phoneme lookups for previously queried words
7. THE Phoneme_Analyzer SHALL pass comparison results to the Scoring_Engine

### Requirement 5: Pronunciation Scoring

**User Story:** As a user, I want to receive a numerical score for my pronunciation, so that I can track my progress.

#### Acceptance Criteria

1. WHEN phoneme comparison results are received, THE Scoring_Engine SHALL calculate an Accuracy_Score between 0 and 100
2. THE Scoring_Engine SHALL weight phoneme matches higher than phoneme substitutions
3. THE Scoring_Engine SHALL penalize missing phonemes and extra phonemes
4. THE Scoring_Engine SHALL return the Accuracy_Score along with detailed phoneme-level results
5. THE Scoring_Engine SHALL complete scoring within 500 milliseconds

### Requirement 6: AI-Powered Feedback Generation

**User Story:** As a user, I want to receive helpful correction tips, so that I can improve my pronunciation.

#### Acceptance Criteria

1. WHEN phoneme comparison results indicate errors, THE Feedback_Generator SHALL generate correction tips using an LLM
2. THE Feedback_Generator SHALL use Gemini or Groq API for generating feedback
3. THE Feedback_Generator SHALL provide specific guidance on how to correct mispronounced phonemes
4. WHEN all phonemes are correct, THE Feedback_Generator SHALL return encouraging feedback
5. THE Feedback_Generator SHALL complete feedback generation within 2 seconds
6. WHEN the LLM API is unavailable, THE Feedback_Generator SHALL return generic fallback feedback

### Requirement 7: Audio Mode

**User Story:** As a user, I want to practice pronunciation in Audio Mode, so that I can focus on specific words or phrases.

#### Acceptance Criteria

1. WHEN Audio Mode is selected, THE Frontend_Client SHALL display an interface for recording or uploading audio
2. THE Frontend_Client SHALL allow the user to specify a Target_Word
3. WHEN a Pronunciation_Attempt is submitted, THE Backend_API SHALL process the audio and return results
4. THE Frontend_Client SHALL display the Accuracy_Score, phoneme comparison, and correction tips
5. THE Frontend_Client SHALL visually highlight incorrect phonemes with error indicators

### Requirement 8: Image Mode

**User Story:** As a user, I want to practice pronunciation using images, so that I can learn vocabulary in context.

#### Acceptance Criteria

1. WHEN Image Mode is selected, THE Frontend_Client SHALL allow the user to upload an image
2. THE Backend_API SHALL detect the primary object in the image
3. THE Backend_API SHALL set the detected object name as the Target_Word
4. THE Frontend_Client SHALL prompt the user to pronounce the Target_Word
5. WHEN a Pronunciation_Attempt is submitted, THE system SHALL evaluate pronunciation as in Audio Mode

### Requirement 9: Game Mode

**User Story:** As a user, I want to practice pronunciation in a gamified environment, so that learning is more engaging.

#### Acceptance Criteria

1. WHEN Game Mode is selected, THE Frontend_Client SHALL display a random Target_Word
2. THE Frontend_Client SHALL display a countdown timer for each pronunciation challenge
3. THE Frontend_Client SHALL track and display cumulative scores across multiple attempts
4. WHEN the timer expires, THE Frontend_Client SHALL move to the next Target_Word
5. THE Frontend_Client SHALL display a leaderboard showing top scores
6. THE Backend_API SHALL store game scores in the database

### Requirement 10: User and Attempt Tracking

**User Story:** As a user, I want my pronunciation attempts saved, so that I can review my progress over time.

#### Acceptance Criteria

1. THE Backend_API SHALL store user information in a database
2. WHEN a Pronunciation_Attempt is completed, THE Backend_API SHALL store the attempt details including Target_Word, Accuracy_Score, and timestamp
3. THE Backend_API SHALL associate each Pronunciation_Attempt with a user
4. THE Backend_API SHALL provide an endpoint to retrieve a user's pronunciation history
5. THE Backend_API SHALL provide an endpoint to retrieve aggregate statistics for a user

### Requirement 11: API Endpoints

**User Story:** As a frontend developer, I want well-defined API endpoints, so that I can integrate the frontend with the backend.

#### Acceptance Criteria

1. THE Backend_API SHALL provide a POST endpoint for pronunciation evaluation accepting audio and Target_Word
2. THE Backend_API SHALL provide a POST endpoint for image-based pronunciation accepting image files
3. THE Backend_API SHALL provide a GET endpoint for retrieving user pronunciation history
4. THE Backend_API SHALL provide a GET endpoint for retrieving leaderboard data
5. THE Backend_API SHALL return responses in JSON format
6. WHEN an API request fails, THE Backend_API SHALL return appropriate HTTP status codes and error messages

### Requirement 12: Performance Optimization

**User Story:** As a user, I want fast response times, so that I can practice pronunciation without delays.

#### Acceptance Criteria

1. THE Backend_API SHALL respond to pronunciation evaluation requests within 6 seconds for audio up to 5 seconds in length
2. THE Backend_API SHALL cache CMU_Dictionary phoneme lookups to reduce processing time
3. THE Backend_API SHALL use a small or base Whisper model to optimize transcription speed
4. THE Backend_API SHALL implement request timeouts to prevent hanging requests
5. WHEN system load is high, THE Backend_API SHALL return a 503 status code with retry-after information

### Requirement 13: Frontend User Interface

**User Story:** As a user, I want an intuitive interface, so that I can easily navigate and use the pronunciation coach.

#### Acceptance Criteria

1. THE Frontend_Client SHALL provide a mode selector for Audio, Image, and Game modes
2. THE Frontend_Client SHALL display pronunciation results with visual phoneme comparison
3. THE Frontend_Client SHALL use color coding to indicate correct and incorrect phonemes
4. THE Frontend_Client SHALL display loading indicators during processing
5. THE Frontend_Client SHALL be responsive and work on desktop and mobile devices
6. THE Frontend_Client SHALL display error messages when operations fail

### Requirement 14: Error Handling

**User Story:** As a user, I want clear error messages, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN audio input is invalid, THE system SHALL display a message indicating the audio format or duration issue
2. WHEN speech recognition fails, THE system SHALL display a message asking the user to speak more clearly
3. WHEN a Target_Word is not in the CMU_Dictionary, THE system SHALL display a message indicating the word is not supported
4. WHEN the LLM API fails, THE system SHALL still provide pronunciation scores with generic feedback
5. WHEN the backend is unreachable, THE Frontend_Client SHALL display a connection error message

### Requirement 15: Deployment Configuration

**User Story:** As a developer, I want clear deployment configurations, so that I can deploy the system to production.

#### Acceptance Criteria

1. THE Frontend_Client SHALL be deployable to Vercel
2. THE Backend_API SHALL be deployable to Render or Railway
3. THE system SHALL use environment variables for API keys and configuration
4. THE Backend_API SHALL include CORS configuration to allow Frontend_Client requests
5. THE deployment configuration SHALL include health check endpoints for monitoring
