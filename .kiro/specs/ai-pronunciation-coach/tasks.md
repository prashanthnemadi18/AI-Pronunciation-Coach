# Implementation Plan: AI Pronunciation Coach

## Overview

This implementation plan breaks down the AI Pronunciation Coach system into discrete coding tasks. The system consists of a FastAPI backend with seven core processing modules, a React + TypeScript frontend with three interaction modes, database integration, and deployment configuration. Tasks are ordered to build incrementally, starting with backend infrastructure, then frontend components, followed by integration and deployment.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create backend directory with FastAPI project structure
  - Create frontend directory with React + TypeScript + Vite
  - Set up virtual environment and install Python dependencies (FastAPI, SQLAlchemy, pydub/librosa, openai-whisper, requests)
  - Install frontend dependencies (React, TypeScript, Tailwind CSS, Axios, React Router)
  - Create .env.example files for both backend and frontend
  - Set up .gitignore files
  - _Requirements: 15.3_

- [x] 2. Implement database models and setup
  - [x] 2.1 Create SQLAlchemy models for users, pronunciation_attempts, and game_scores tables
    - Define User model with id, username, created_at fields
    - Define PronunciationAttempt model with all required fields
    - Define GameScore model with scoring fields
    - Add foreign key relationships
    - _Requirements: 10.1, 10.2, 10.3_
  
  - [x] 2.2 Create database initialization and connection module
    - Implement database connection with SQLite for development
    - Add PostgreSQL support for production via DATABASE_URL env var
    - Create database initialization function
    - Add indexes for performance optimization
    - _Requirements: 10.1_
  
  - [ ]* 2.3 Write property test for database consistency
    - **Property 5: Database Consistency**
    - **Validates: Requirements 10.2, 10.3**

- [x] 3. Implement Audio Input Module
  - [x] 3.1 Create AudioInputModule class with audio validation
    - Implement accept_recording method for microphone audio
    - Implement accept_upload method for file uploads
    - Validate audio formats (WAV, MP3, M4A)
    - Validate audio duration (max 5 seconds)
    - Return AudioData object or validation errors
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [ ]* 3.2 Write property test for audio duration validation
    - **Property 1: Audio Duration Validation**
    - **Validates: Requirements 1.3**

- [x] 4. Implement Audio Processing Module
  - [x] 4.1 Create AudioProcessor class with audio normalization and noise reduction
    - Implement normalize_volume using pydub or librosa
    - Implement remove_noise for background noise reduction
    - Implement convert_format to prepare audio for Whisper
    - Ensure processing completes within 2 seconds
    - Add error handling with descriptive messages
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [ ]* 4.2 Write unit tests for audio processing functions
    - Test volume normalization with various input levels
    - Test noise reduction effectiveness
    - Test format conversion accuracy
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Implement Speech Recognition Module
  - [x] 5.1 Create SpeechRecognizer class with Whisper integration
    - Initialize Whisper model (base or small size)
    - Implement transcribe method using Whisper API or local model
    - Handle no speech detected errors
    - Ensure transcription completes within 3 seconds
    - Implement singleton pattern for model loading
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [ ]* 5.2 Write unit tests for speech recognition
    - Test transcription with sample audio files
    - Test error handling for silent audio
    - Test performance with 5-second audio clips
    - _Requirements: 3.1, 3.3, 3.5_

- [ ] 6. Checkpoint - Ensure audio pipeline tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement Phoneme Analysis Module
  - [x] 7.1 Create PhonemeAnalyzer class with CMU Dictionary integration
    - Load CMU Pronunciation Dictionary
    - Implement get_expected_phonemes to retrieve phonemes for target word
    - Implement get_actual_phonemes to convert transcribed text to phonemes
    - Implement compare_phonemes to identify matches, substitutions, missing, and extra phonemes
    - Implement in-memory cache for phoneme lookups
    - Handle words not found in dictionary with appropriate errors
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
  
  - [ ]* 7.2 Write property test for phoneme comparison completeness
    - **Property 3: Phoneme Comparison Completeness**
    - **Validates: Requirements 4.3, 4.4**
  
  - [ ]* 7.3 Write property test for phoneme cache consistency
    - **Property 7: Phoneme Cache Consistency**
    - **Validates: Requirements 4.6**
  
  - [ ]* 7.4 Write unit tests for phoneme analysis
    - Test phoneme extraction for common words
    - Test comparison logic with various phoneme sequences
    - Test cache functionality
    - Test error handling for unknown words
    - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [x] 8. Implement Scoring Engine Module
  - [x] 8.1 Create ScoringEngine class with accuracy calculation
    - Implement calculate_score method using phoneme comparison results
    - Weight matches positively
    - Penalize substitutions, missing, and extra phonemes
    - Ensure score is always between 0-100
    - Complete scoring within 500ms
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ]* 8.2 Write property test for score range invariant
    - **Property 2: Score Range Invariant**
    - **Validates: Requirements 5.1**
  
  - [ ]* 8.3 Write unit tests for scoring algorithm
    - Test scoring with perfect pronunciation
    - Test scoring with various error types
    - Test edge cases (empty phonemes, all wrong)
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 9. Implement Feedback Generation Module
  - [x] 9.1 Create FeedbackGenerator class with LLM integration
    - Initialize with LLM provider (Gemini or Groq) and API key
    - Implement generate_feedback method with prompt construction
    - Create specific correction tips for mispronounced phonemes
    - Provide encouraging feedback for correct pronunciation
    - Implement fallback feedback for LLM API failures
    - Ensure feedback generation completes within 2 seconds
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  
  - [ ]* 9.2 Write property test for feedback generation fallback
    - **Property 8: Feedback Generation Fallback**
    - **Validates: Requirements 6.6, 14.4**
  
  - [ ]* 9.3 Write unit tests for feedback generation
    - Test prompt construction
    - Test fallback feedback mechanism
    - Test LLM API error handling
    - _Requirements: 6.3, 6.4, 6.6_

- [x] 10. Implement Image Detection Module
  - [x] 10.1 Create ImageDetector class with object detection
    - Implement detect_object method using Gemini Vision API or YOLO
    - Implement get_primary_object to select most prominent object
    - Return detected object name and confidence score
    - Handle multiple objects in image
    - _Requirements: 8.2, 8.3_
  
  - [ ]* 10.2 Write unit tests for image detection
    - Test object detection with sample images
    - Test primary object selection logic
    - Test error handling for invalid images
    - _Requirements: 8.2, 8.3_

- [ ] 11. Checkpoint - Ensure all backend modules pass tests
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Implement core API endpoints
  - [x] 12.1 Create FastAPI application with CORS middleware
    - Initialize FastAPI app
    - Configure CORS with environment variable for allowed origins
    - Set up request timeout handling
    - Add global exception handlers
    - _Requirements: 15.4, 12.4_
  
  - [x] 12.2 Implement POST /api/pronunciation/evaluate endpoint
    - Accept audio data and target word
    - Orchestrate full processing pipeline (Audio Input → Processing → Recognition → Phoneme Analysis → Scoring → Feedback)
    - Return comprehensive evaluation results
    - Store attempt in database
    - Ensure total processing time ≤ 6 seconds
    - _Requirements: 11.1, 10.2, 12.1_
  
  - [x] 12.3 Implement POST /api/pronunciation/image endpoint
    - Accept image file upload
    - Detect primary object using ImageDetector
    - Return detected object as target word
    - _Requirements: 11.2, 8.2, 8.3_
  
  - [x] 12.4 Implement GET /api/user/{user_id}/history endpoint
    - Retrieve user's pronunciation attempts from database
    - Calculate aggregate statistics (total attempts, average score)
    - Return paginated results
    - _Requirements: 11.3, 10.4_
  
  - [x] 12.5 Implement GET /api/leaderboard endpoint
    - Retrieve top game scores from database
    - Join with users table for usernames
    - Return sorted leaderboard data
    - _Requirements: 11.4, 9.5_
  
  - [x] 12.6 Implement GET /api/health endpoint
    - Check database connection status
    - Check Whisper model availability
    - Check LLM API availability
    - Return health status with timestamp
    - _Requirements: 15.5_
  
  - [ ]* 12.7 Write property test for processing time bounds
    - **Property 4: Processing Time Bounds**
    - **Validates: Requirements 2.5, 3.5, 5.5, 6.5, 12.1**
  
  - [ ]* 12.8 Write property test for error response format
    - **Property 6: Error Response Format**
    - **Validates: Requirements 11.6, 14.1, 14.2, 14.3, 14.4, 14.5**
  
  - [ ]* 12.9 Write integration tests for API endpoints
    - Test /evaluate endpoint with sample audio
    - Test /image endpoint with sample images
    - Test /history endpoint with test data
    - Test /leaderboard endpoint
    - Test error responses for all endpoints
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.6_

- [x] 13. Implement frontend core components and routing
  - [x] 13.1 Set up React Router and main App component
    - Configure React Router with routes for different modes
    - Create App component with navigation
    - Set up Tailwind CSS configuration
    - Create global state management (Context or Zustand)
    - _Requirements: 13.1_
  
  - [x] 13.2 Create ModeSelector component
    - Display buttons for Audio, Image, and Game modes
    - Handle mode switching
    - Highlight currently selected mode
    - _Requirements: 13.1_
  
  - [x] 13.3 Create API client service
    - Implement PronunciationAPI class with all endpoint methods
    - Configure Axios with base URL from environment variable
    - Add request/response interceptors for error handling
    - Implement loading states
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 14. Implement Audio Mode components
  - [x] 14.1 Create AudioRecorder component
    - Implement start/stop recording functionality using MediaRecorder API
    - Display recording status indicator
    - Show duration counter
    - Validate max 5 seconds duration
    - Provide audio preview playback
    - _Requirements: 1.1, 1.5, 7.1_
  
  - [x] 14.2 Create AudioUploader component
    - Implement file upload with drag-and-drop
    - Validate file formats (WAV, MP3, M4A)
    - Display file name and size
    - _Requirements: 1.2, 7.1_
  
  - [x] 14.3 Create TargetWordInput component
    - Input field for target word
    - Validation for non-empty input
    - _Requirements: 7.2_
  
  - [x] 14.4 Create ResultsDisplay component
    - Display accuracy score with visual gauge or progress bar
    - Show phoneme-by-phoneme comparison table
    - Color code correct (green) and incorrect (red) phonemes
    - Display feedback tips and encouragement
    - _Requirements: 7.4, 7.5, 13.2, 13.3_
  
  - [x] 14.5 Create AudioMode page component
    - Integrate AudioRecorder, AudioUploader, TargetWordInput components
    - Handle form submission to /evaluate endpoint
    - Display loading indicator during processing
    - Show ResultsDisplay on completion
    - Handle and display errors
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 13.4, 14.5_

- [x] 15. Implement Image Mode components
  - [x] 15.1 Create ImageUploader component for Image Mode
    - Implement image file upload with preview
    - Validate image formats (JPEG, PNG)
    - Display uploaded image
    - _Requirements: 8.1_
  
  - [x] 15.2 Create ObjectDetectionDisplay component
    - Show detected object name
    - Display confidence score
    - Prompt user to pronounce the word
    - _Requirements: 8.3, 8.4_
  
  - [x] 15.3 Create ImageMode page component
    - Integrate ImageUploader component
    - Call /image endpoint for object detection
    - Display ObjectDetectionDisplay with results
    - Integrate AudioRecorder for pronunciation attempt
    - Call /evaluate endpoint with detected word
    - Display ResultsDisplay with pronunciation results
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 16. Implement Game Mode components
  - [x] 16.1 Create GameTimer component
    - Display countdown timer (30 seconds per word)
    - Trigger callback when timer expires
    - Visual progress indicator
    - _Requirements: 9.2, 9.4_
  
  - [x] 16.2 Create ScoreTracker component
    - Display current cumulative score
    - Display number of words attempted
    - Animate score updates
    - _Requirements: 9.3_
  
  - [x] 16.3 Create Leaderboard component
    - Fetch and display leaderboard data from /leaderboard endpoint
    - Show top scores with usernames
    - Highlight current user's position
    - _Requirements: 9.5_
  
  - [x] 16.4 Create GameMode page component
    - Generate random target words from predefined list
    - Display current target word prominently
    - Integrate GameTimer component
    - Integrate AudioRecorder for pronunciation attempts
    - Call /evaluate endpoint and update cumulative score
    - Integrate ScoreTracker component
    - Handle timer expiration and move to next word
    - Display Leaderboard at end of game
    - Store final game score via API
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

- [ ] 17. Checkpoint - Ensure frontend components render correctly
  - Ensure all tests pass, ask the user if questions arise.

- [x] 18. Implement error handling and loading states
  - [x] 18.1 Create ErrorMessage component
    - Display user-friendly error messages
    - Map error codes to readable messages
    - Provide retry or dismiss actions
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_
  
  - [x] 18.2 Create LoadingSpinner component
    - Display loading indicator during API calls
    - Show processing status messages
    - _Requirements: 13.4_
  
  - [x] 18.3 Add error handling to all API calls
    - Catch network errors and display connection error message
    - Handle API error responses with appropriate messages
    - Implement retry logic for transient failures
    - _Requirements: 14.5_

- [x] 19. Implement responsive design
  - [x] 19.1 Add responsive styles to all components
    - Define Tailwind breakpoints (mobile: 640px, tablet: 768px, desktop: 1024px)
    - Make layouts responsive with flexbox/grid
    - Ensure touch-friendly button sizes on mobile
    - Test on different screen sizes
    - _Requirements: 13.5_

- [ ] 20. Set up backend deployment configuration
  - [ ] 20.1 Create requirements.txt with all Python dependencies
    - List all required packages with versions
    - _Requirements: 15.2_
  
  - [ ] 20.2 Create render.yaml or railway.json deployment config
    - Configure web service with Python environment
    - Set build and start commands
    - Define environment variables
    - Configure health check endpoint
    - _Requirements: 15.2, 15.3, 15.4, 15.5_
  
  - [ ] 20.3 Create Dockerfile for containerized deployment (optional)
    - Multi-stage build for optimization
    - Install dependencies and copy application code
    - Expose port and define start command
    - _Requirements: 15.2_
  
  - [ ] 20.4 Add environment variable documentation
    - Document all required environment variables in README
    - Provide example values in .env.example
    - _Requirements: 15.3_

- [ ] 21. Set up frontend deployment configuration
  - [ ] 21.1 Create vercel.json configuration
    - Configure build settings
    - Set output directory
    - Define environment variables
    - _Requirements: 15.1_
  
  - [ ] 21.2 Update frontend to use environment variable for API URL
    - Use VITE_API_BASE_URL for backend endpoint
    - Provide fallback for local development
    - _Requirements: 15.1, 15.3_

- [ ] 22. Create documentation and README files
  - [ ] 22.1 Create backend README.md
    - Document setup instructions
    - List API endpoints with examples
    - Explain environment variables
    - Provide local development guide
    - _Requirements: 15.3_
  
  - [ ] 22.2 Create frontend README.md
    - Document setup instructions
    - Explain component architecture
    - Provide local development guide
    - List environment variables
    - _Requirements: 15.3_
  
  - [ ] 22.3 Create root README.md
    - Provide project overview
    - Link to backend and frontend READMEs
    - Include deployment instructions
    - Add architecture diagram
    - _Requirements: 15.1, 15.2_

- [ ] 23. Final integration and testing
  - [ ] 23.1 Test complete end-to-end flow for Audio Mode
    - Record audio, submit for evaluation, verify results display
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [ ] 23.2 Test complete end-to-end flow for Image Mode
    - Upload image, detect object, pronounce word, verify results
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ] 23.3 Test complete end-to-end flow for Game Mode
    - Play game, complete multiple words, verify score tracking and leaderboard
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_
  
  - [ ]* 23.4 Run all property-based tests
    - Execute all property tests to validate correctness properties
    - Fix any failures discovered
  
  - [ ]* 23.5 Run all unit and integration tests
    - Execute full test suite
    - Verify code coverage
    - Fix any failing tests

- [ ] 24. Final checkpoint - Ensure all tests pass and system is ready for deployment
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Backend uses Python with FastAPI, frontend uses TypeScript with React
- The implementation builds incrementally: backend modules → API endpoints → frontend components → integration → deployment
