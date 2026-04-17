import React, { useEffect, useState } from 'react';

interface ScoreTrackerProps {
  currentScore: number;
  wordsAttempted: number;
  lastScore?: number;
}

const ScoreTracker: React.FC<ScoreTrackerProps> = ({
  currentScore,
  wordsAttempted,
  lastScore,
}) => {
  const [animateScore, setAnimateScore] = useState(false);

  useEffect(() => {
    if (lastScore !== undefined) {
      setAnimateScore(true);
      const timer = setTimeout(() => setAnimateScore(false), 500);
      return () => clearTimeout(timer);
    }
  }, [currentScore, lastScore]);

  const averageScore = wordsAttempted > 0 ? (currentScore / wordsAttempted).toFixed(1) : '0.0';

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 shadow-lg border-2 border-purple-200">
      <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
        📊 Your Score
      </h3>

      <div className="grid grid-cols-2 gap-4">
        {/* Total Score */}
        <div className="bg-white rounded-lg p-4 text-center">
          <p className="text-sm text-gray-600 mb-1">Total Score</p>
          <p className={`text-4xl font-bold text-purple-600 ${animateScore ? 'animate-bounce' : ''}`}>
            {currentScore}
          </p>
          {lastScore !== undefined && lastScore > 0 && (
            <p className="text-xs text-green-600 mt-1">
              +{lastScore.toFixed(0)}
            </p>
          )}
        </div>

        {/* Words Attempted */}
        <div className="bg-white rounded-lg p-4 text-center">
          <p className="text-sm text-gray-600 mb-1">Words</p>
          <p className="text-4xl font-bold text-blue-600">
            {wordsAttempted}
          </p>
        </div>
      </div>

      {/* Average Score */}
      <div className="mt-4 bg-white rounded-lg p-3 text-center">
        <p className="text-sm text-gray-600">Average Score</p>
        <p className="text-2xl font-bold text-indigo-600">
          {averageScore}
        </p>
      </div>

      {/* Encouragement */}
      {wordsAttempted > 0 && (
        <div className="mt-4 text-center">
          {parseFloat(averageScore) >= 90 && (
            <p className="text-sm text-green-600 font-semibold">🌟 Excellent work!</p>
          )}
          {parseFloat(averageScore) >= 70 && parseFloat(averageScore) < 90 && (
            <p className="text-sm text-blue-600 font-semibold">👍 Great job!</p>
          )}
          {parseFloat(averageScore) < 70 && (
            <p className="text-sm text-yellow-600 font-semibold">💪 Keep practicing!</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ScoreTracker;
