import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { pronunciationAPI } from '../services/api';
import { getRandomWord } from '../utils/wordList';
import GameTimer from '../components/GameTimer';
import ScoreTracker from '../components/ScoreTracker';
import Leaderboard from '../components/Leaderboard';
import AudioRecorder from '../components/AudioRecorder';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

type GameState = 'ready' | 'playing' | 'finished';

const GameMode: React.FC = () => {
  const { userId } = useApp();
  const [gameState, setGameState] = useState<GameState>('ready');
  const [currentWord, setCurrentWord] = useState<string>('');
  const [totalScore, setTotalScore] = useState(0);
  const [wordsAttempted, setWordsAttempted] = useState(0);
  const [lastScore, setLastScore] = useState<number | undefined>(undefined);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [timerActive, setTimerActive] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  const TIMER_DURATION = 30; // seconds per word
  const WORDS_PER_GAME = 5;

  useEffect(() => {
    if (gameState === 'playing' && !currentWord) {
      nextWord();
    }
  }, [gameState]);

  const startGame = () => {
    setGameState('playing');
    setTotalScore(0);
    setWordsAttempted(0);
    setLastScore(undefined);
    setError(null);
    setShowLeaderboard(false);
    nextWord();
  };

  const nextWord = () => {
    if (wordsAttempted >= WORDS_PER_GAME) {
      finishGame();
      return;
    }

    const word = getRandomWord();
    setCurrentWord(word);
    setAudioBlob(null);
    setTimerActive(true);
    setError(null);
  };

  const handleTimeUp = () => {
    setTimerActive(false);
    if (!audioBlob) {
      setError('Time is up! Moving to next word...');
      setTimeout(() => {
        setWordsAttempted((prev) => prev + 1);
        nextWord();
      }, 2000);
    }
  };

  const handleRecordingComplete = (blob: Blob) => {
    setAudioBlob(blob);
    setTimerActive(false);
  };

  const handleSubmit = async () => {
    if (!audioBlob) {
      setError('Please record audio first');
      return;
    }

    setIsEvaluating(true);
    setError(null);

    try {
      const result = await pronunciationAPI.evaluatePronunciation(
        audioBlob,
        currentWord,
        userId,
        'game'
      );

      const score = result.accuracy_score;
      setLastScore(score);
      setTotalScore((prev) => prev + score);
      setWordsAttempted((prev) => prev + 1);

      // Move to next word after showing score
      setTimeout(() => {
        nextWord();
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate pronunciation');
      setTimerActive(true);
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleSkip = () => {
    setWordsAttempted((prev) => prev + 1);
    nextWord();
  };

  const finishGame = async () => {
    setGameState('finished');
    setTimerActive(false);
    setShowLeaderboard(true);

    // Save game score to backend (optional - could be done via API)
    // For now, the leaderboard will show cumulative scores from all attempts
  };

  const resetGame = () => {
    setGameState('ready');
    setCurrentWord('');
    setTotalScore(0);
    setWordsAttempted(0);
    setLastScore(undefined);
    setAudioBlob(null);
    setError(null);
    setTimerActive(false);
    setShowLeaderboard(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Game Mode</h2>
        <p className="text-gray-600 mb-8">
          Race against time! Pronounce {WORDS_PER_GAME} words correctly to earn points
        </p>

        {/* Ready State */}
        {gameState === 'ready' && (
          <div className="text-center space-y-6">
            <div className="text-6xl mb-4">🎮</div>
            <h3 className="text-2xl font-bold text-gray-800">Ready to Play?</h3>
            <p className="text-gray-600">
              You'll have {TIMER_DURATION} seconds to pronounce each word.
              <br />
              Try to get the highest score possible!
            </p>
            <button
              onClick={startGame}
              className="px-12 py-4 rounded-lg font-bold text-xl bg-gradient-to-r from-green-500 to-green-600 text-white hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
            >
              Start Game
            </button>

            {/* Show Leaderboard */}
            <div className="mt-8">
              <Leaderboard currentUserId={userId} />
            </div>
          </div>
        )}

        {/* Playing State */}
        {gameState === 'playing' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Score Tracker */}
              <div className="md:col-span-1">
                <ScoreTracker
                  currentScore={totalScore}
                  wordsAttempted={wordsAttempted}
                  lastScore={lastScore}
                />
              </div>

              {/* Main Game Area */}
              <div className="md:col-span-2 space-y-6">
                {/* Progress */}
                <div className="text-center">
                  <p className="text-sm text-gray-600">
                    Word {wordsAttempted + 1} of {WORDS_PER_GAME}
                  </p>
                </div>

                {/* Current Word */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 border-2 border-blue-200">
                  <p className="text-center text-sm text-gray-600 mb-2">Pronounce this word:</p>
                  <h3 className="text-5xl font-bold text-center text-blue-600 capitalize">
                    {currentWord}
                  </h3>
                </div>

                {/* Timer */}
                <GameTimer
                  duration={TIMER_DURATION}
                  onTimeUp={handleTimeUp}
                  isActive={timerActive}
                />

                {/* Audio Recorder */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <AudioRecorder
                    onRecordingComplete={handleRecordingComplete}
                    maxDuration={5}
                  />
                </div>

                {/* Error Display */}
                {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

                {/* Action Buttons */}
                <div className="flex justify-center gap-4">
                  <button
                    onClick={handleSubmit}
                    disabled={!audioBlob || isEvaluating}
                    className={`
                      px-8 py-3 rounded-lg font-bold text-lg transition-all duration-200
                      ${
                        audioBlob && !isEvaluating
                          ? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:shadow-lg transform hover:-translate-y-0.5'
                          : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }
                    `}
                  >
                    {isEvaluating ? 'Evaluating...' : 'Submit'}
                  </button>

                  <button
                    onClick={handleSkip}
                    disabled={isEvaluating}
                    className="px-8 py-3 rounded-lg font-bold text-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition-all duration-200"
                  >
                    Skip
                  </button>
                </div>

                {/* Loading Spinner */}
                {isEvaluating && <LoadingSpinner message="Evaluating..." size="small" />}
              </div>
            </div>
          </div>
        )}

        {/* Finished State */}
        {gameState === 'finished' && (
          <div className="text-center space-y-6">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-3xl font-bold text-gray-800">Game Over!</h3>
            
            {/* Final Score */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-8 border-2 border-purple-200">
              <p className="text-lg text-gray-600 mb-2">Your Final Score</p>
              <p className="text-6xl font-bold text-purple-600 mb-4">{totalScore.toFixed(0)}</p>
              <p className="text-gray-600">
                Average: {(totalScore / wordsAttempted).toFixed(1)} per word
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-center gap-4">
              <button
                onClick={startGame}
                className="px-8 py-3 rounded-lg font-bold text-lg bg-gradient-to-r from-green-500 to-green-600 text-white hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
              >
                Play Again
              </button>
              <button
                onClick={resetGame}
                className="px-8 py-3 rounded-lg font-bold text-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition-all duration-200"
              >
                Back to Menu
              </button>
            </div>

            {/* Leaderboard */}
            {showLeaderboard && (
              <div className="mt-8">
                <Leaderboard currentUserId={userId} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default GameMode;
