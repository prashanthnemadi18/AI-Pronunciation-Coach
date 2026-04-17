# AI Pronunciation Coach - Frontend

React + TypeScript frontend for the AI Pronunciation Coach application.

## Features

- **Audio Mode**: Record or upload audio to practice pronunciation
- **Image Mode**: Upload images and practice pronouncing detected objects
- **Game Mode**: Gamified pronunciation practice with timer and leaderboard
- Real-time pronunciation feedback with phoneme-level analysis
- Responsive design for mobile, tablet, and desktop
- Beautiful UI with Tailwind CSS

## Tech Stack

- React 18
- TypeScript
- Vite (build tool)
- React Router (navigation)
- Axios (HTTP client)
- Tailwind CSS (styling)

## Prerequisites

- Node.js 16+ and npm
- Backend API running (see backend README)

## Setup Instructions

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8000)

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The app will be available at http://localhost:5173

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Component Architecture

```
src/
├── components/          # Reusable UI components
│   ├── AudioRecorder.tsx
│   ├── AudioUploader.tsx
│   ├── ErrorMessage.tsx
│   ├── GameTimer.tsx
│   ├── ImageUploader.tsx
│   ├── Leaderboard.tsx
│   ├── LoadingSpinner.tsx
│   ├── ModeSelector.tsx
│   ├── ObjectDetectionDisplay.tsx
│   ├── ResultsDisplay.tsx
│   ├── ScoreTracker.tsx
│   └── TargetWordInput.tsx
├── pages/               # Page components
│   ├── AudioMode.tsx
│   ├── ImageMode.tsx
│   └── GameMode.tsx
├── context/             # React Context for state management
│   └── AppContext.tsx
├── services/            # API client
│   └── api.ts
├── types/               # TypeScript type definitions
│   └── index.ts
├── utils/               # Utility functions
│   └── wordList.ts
├── App.tsx              # Main app component with routing
└── main.tsx             # Entry point
```

## Key Features

### Audio Mode
- Record audio using microphone
- Upload audio files (WAV, MP3, M4A)
- Enter target word for pronunciation practice
- View detailed phoneme-level feedback
- See accuracy score with visual indicators

### Image Mode
- Upload images (JPEG, PNG)
- Automatic object detection
- Practice pronouncing detected objects
- Step-by-step guided workflow

### Game Mode
- Timed pronunciation challenges (30s per word)
- Score tracking across multiple words
- Real-time leaderboard
- 5 words per game session

## Responsive Design

The application is fully responsive with breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

All components adapt to different screen sizes with touch-friendly controls on mobile.

## Error Handling

The app includes comprehensive error handling:
- Network connection errors
- Invalid audio/image formats
- API errors with user-friendly messages
- Retry mechanisms for failed requests

## Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   cd frontend
   vercel
   ```

3. Set environment variables in Vercel dashboard:
   - `VITE_API_BASE_URL`: Your production backend URL

### Manual Build

```bash
npm run build
```

The built files will be in the `dist/` directory. Deploy these to any static hosting service.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | http://localhost:8000 |

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development Notes

- The app uses React Context for global state management
- API calls are centralized in `services/api.ts`
- All components are TypeScript with proper type definitions
- Tailwind CSS is used for all styling
- No external UI libraries (custom components)

## Troubleshooting

**Issue: Cannot connect to backend**
- Ensure backend is running on the correct port
- Check `VITE_API_BASE_URL` in `.env`
- Verify CORS is configured in backend

**Issue: Microphone not working**
- Check browser permissions for microphone access
- Use HTTPS in production (required for microphone API)

**Issue: Image upload fails**
- Ensure image is JPEG or PNG format
- Check file size is under 10MB
- Verify backend has GEMINI_API_KEY configured

## License

MIT
