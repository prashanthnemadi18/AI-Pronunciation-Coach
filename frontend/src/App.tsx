import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import ModeSelector from './components/ModeSelector';
import AudioMode from './pages/AudioMode';
import ImageMode from './pages/ImageMode';
import GameMode from './pages/GameMode';

function Navigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const isHome = location.pathname === '/';

  if (isHome) return null;

  return (
    <button
      onClick={() => navigate('/')}
      className="mb-8 inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors group"
    >
      <svg className="w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
      </svg>
      <span className="font-medium">Back to Home</span>
    </button>
  );
}

function AppContent() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-12 max-w-7xl">
        <header className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl mb-6 shadow-lg">
            <span className="text-4xl">🎤</span>
          </div>
          <h1 className="text-6xl font-bold text-gray-900 mb-4">
            AI Pronunciation Coach
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Master your pronunciation with AI-powered feedback and interactive practice
          </p>
        </header>

        <Navigation />

        <Routes>
          <Route path="/" element={<ModeSelector />} />
          <Route path="/audio" element={<AudioMode />} />
          <Route path="/image" element={<ImageMode />} />
          <Route path="/game" element={<GameMode />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <Router>
        <AppContent />
      </Router>
    </AppProvider>
  );
}

export default App;
