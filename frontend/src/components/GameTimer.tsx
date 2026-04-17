import React, { useState, useEffect, useRef } from 'react';

interface GameTimerProps {
  duration: number; // in seconds
  onTimeUp: () => void;
  isActive: boolean;
}

const GameTimer: React.FC<GameTimerProps> = ({
  duration,
  onTimeUp,
  isActive,
}) => {
  const [timeLeft, setTimeLeft] = useState(duration);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (isActive && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            onTimeUp();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (!isActive && timerRef.current) {
      clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isActive, timeLeft, onTimeUp]);

  useEffect(() => {
    setTimeLeft(duration);
  }, [duration]);

  const percentage = (timeLeft / duration) * 100;
  const isLowTime = timeLeft <= 5;

  const getTimerColor = (): string => {
    if (timeLeft <= 5) return 'text-red-600';
    if (timeLeft <= 10) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getProgressColor = (): string => {
    if (timeLeft <= 5) return 'from-red-500 to-red-600';
    if (timeLeft <= 10) return 'from-yellow-500 to-yellow-600';
    return 'from-green-500 to-green-600';
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <div className={`text-6xl font-bold font-mono ${getTimerColor()} ${isLowTime ? 'animate-pulse' : ''}`}>
          {timeLeft}s
        </div>
        <p className="text-sm text-gray-600 mt-2">Time Remaining</p>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className={`h-4 bg-gradient-to-r ${getProgressColor()} transition-all duration-1000 ease-linear`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>

      {/* Visual Indicator */}
      {isLowTime && (
        <div className="text-center text-red-600 font-semibold animate-bounce">
          ⏰ Hurry up!
        </div>
      )}
    </div>
  );
};

export default GameTimer;
