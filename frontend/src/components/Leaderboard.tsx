import React, { useEffect, useState } from 'react';
import { pronunciationAPI } from '../services/api';
import { LeaderboardEntry } from '../types';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

interface LeaderboardProps {
  currentUserId?: number;
  limit?: number;
}

const Leaderboard: React.FC<LeaderboardProps> = ({
  currentUserId,
  limit = 10,
}) => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLeaderboard();
  }, [limit]);

  const fetchLeaderboard = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await pronunciationAPI.getLeaderboard(limit);
      setEntries(result.leaderboard);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load leaderboard');
    } finally {
      setIsLoading(false);
    }
  };

  const getMedalEmoji = (rank: number): string => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `${rank}`;
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading leaderboard..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchLeaderboard} />;
  }

  if (entries.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <p className="text-gray-600">No leaderboard entries yet. Be the first to play!</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center flex items-center justify-center gap-2">
        <span>🏆</span>
        <span>Leaderboard</span>
      </h3>

      <div className="space-y-2">
        {entries.map((entry, index) => {
          const rank = index + 1;
          const isCurrentUser = currentUserId && entry.user_id === currentUserId;
          const averageScore = entry.words_attempted > 0
            ? (entry.total_score / entry.words_attempted).toFixed(1)
            : '0.0';

          return (
            <div
              key={entry.user_id}
              className={`
                flex items-center gap-4 p-4 rounded-lg transition-all duration-200
                ${isCurrentUser ? 'bg-blue-100 border-2 border-blue-400' : 'bg-gray-50 hover:bg-gray-100'}
              `}
            >
              {/* Rank */}
              <div className="w-12 text-center">
                <span className="text-2xl font-bold">
                  {getMedalEmoji(rank)}
                </span>
              </div>

              {/* User Info */}
              <div className="flex-1">
                <p className={`font-bold ${isCurrentUser ? 'text-blue-800' : 'text-gray-800'}`}>
                  {entry.username || `User ${entry.user_id}`}
                  {isCurrentUser && <span className="ml-2 text-sm">(You)</span>}
                </p>
                <p className="text-sm text-gray-600">
                  {entry.words_attempted} words attempted
                </p>
              </div>

              {/* Scores */}
              <div className="text-right">
                <p className="text-2xl font-bold text-purple-600">
                  {entry.total_score}
                </p>
                <p className="text-xs text-gray-600">
                  Avg: {averageScore}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Refresh Button */}
      <div className="mt-6 text-center">
        <button
          onClick={fetchLeaderboard}
          className="text-blue-600 hover:text-blue-700 font-semibold text-sm"
        >
          🔄 Refresh
        </button>
      </div>
    </div>
  );
};

export default Leaderboard;
