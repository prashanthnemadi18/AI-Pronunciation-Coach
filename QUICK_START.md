# AI Pronunciation Coach - Quick Start Guide

Complete guide to run the AI Pronunciation Coach application locally.

## Prerequisites

- Python 3.10+
- Node.js 16+
- FFmpeg (for audio processing)
- API Keys:
  - Gemini API key (for feedback generation and image detection)
  - OR Groq API key (alternative for feedback generation)

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # Required:
   LLM_API_KEY=your_gemini_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional:
   WHISPER_MODEL_SIZE=base
   LLM_PROVIDER=gemini
   DATABASE_URL=sqlite:///./pronunciation_coach.db
   ```

5. **Start the backend server:**
   ```bash
   python start_server.py
   ```
   
   The backend will be available at: http://localhost:8000

6. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```

## Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env (default should work for local development)
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the frontend dev server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at: http://localhost:5173

## Using the Application

### Audio Mode

1. Navigate to http://localhost:5173/audio
2. Enter a target word (e.g., "hello")
3. Choose to record or upload audio:
   - **Record**: Click "Start Recording", speak the word, click "Stop Recording"
   - **Upload**: Drag and drop an audio file (WAV, MP3, M4A)
4. Click "Evaluate Pronunciation"
5. View your results:
   - Accuracy score
   - Phoneme-by-phoneme comparison
   - Feedback and tips

### Image Mode

1. Navigate to http://localhost:5173/image
2. Upload an image (JPEG or PNG)
3. Wait for object detection
4. Record yourself pronouncing the detected object
5. Click "Evaluate Pronunciation"
6. View your results

### Game Mode

1. Navigate to http://localhost:5173/game
2. Click "Start Game"
3. You'll have 30 seconds per word to:
   - Record your pronunciation
   - Submit for evaluation
   - Or skip to the next word
4. Complete 5 words to finish the game
5. View your final score and leaderboard

## Troubleshooting

### Backend Issues

**Issue: ModuleNotFoundError**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: API key errors**
```bash
# Verify .env file has correct API keys
# Check that LLM_API_KEY or GEMINI_API_KEY is set
```

**Issue: FFmpeg not found**
```bash
# Windows: Download from https://ffmpeg.org/download.html
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### Frontend Issues

**Issue: Cannot connect to backend**
```bash
# Verify backend is running on port 8000
# Check VITE_API_BASE_URL in frontend/.env
# Ensure CORS is configured in backend
```

**Issue: Microphone not working**
```bash
# Check browser permissions for microphone
# Use HTTPS in production (required for microphone API)
# Try a different browser (Chrome recommended)
```

**Issue: Build errors**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## API Endpoints

The backend provides the following endpoints:

- `GET /` - API information
- `POST /api/pronunciation/evaluate` - Evaluate pronunciation
- `POST /api/pronunciation/image` - Detect object in image
- `GET /api/user/{user_id}/history` - Get user history
- `GET /api/leaderboard` - Get leaderboard
- `GET /api/health` - Health check

See `backend/API_ENDPOINTS.md` for detailed documentation.

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Build
```bash
cd frontend
npm run build
```

## Production Deployment

### Backend (Render/Railway)

1. Create a new web service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `LLM_API_KEY`
   - `GEMINI_API_KEY`
   - `DATABASE_URL` (if using PostgreSQL)
   - `CORS_ORIGINS` (your frontend URL)

### Frontend (Vercel)

1. Install Vercel CLI: `npm install -g vercel`
2. Deploy: `cd frontend && vercel`
3. Set environment variable:
   - `VITE_API_BASE_URL`: Your production backend URL

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Audio Mode  │  │  Image Mode  │  │  Game Mode   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Core Processing Pipeline                 │   │
│  │  Audio Input → Audio Processing → Speech Recognition │   │
│  │  → Phoneme Analysis → Scoring → Feedback Generation  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Database   │  │ Whisper API  │  │   LLM API    │      │
│  │ (SQLite/PG)  │  │              │  │ (Gemini/Groq)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Features

- ✅ Audio Mode: Record or upload audio for pronunciation practice
- ✅ Image Mode: Upload images and practice pronouncing detected objects
- ✅ Game Mode: Timed pronunciation challenges with leaderboard
- ✅ Real-time phoneme-level analysis
- ✅ AI-powered feedback and tips
- ✅ Responsive design for mobile/tablet/desktop
- ✅ Comprehensive error handling
- ✅ User history tracking
- ✅ Score tracking and leaderboards

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend/README.md and frontend/README.md
3. Check API_ENDPOINTS.md for API documentation
4. Review implementation summaries in each directory

## License

MIT
