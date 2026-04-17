import React from 'react';

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss, onRetry }) => {
  // Map common error messages to user-friendly versions
  const getFriendlyMessage = (msg: string): string => {
    const errorMap: Record<string, string> = {
      'Invalid audio format': 'Please upload a valid audio file (WAV, MP3, or M4A)',
      'Audio duration exceeded': 'Audio must be 5 seconds or less',
      'No speech detected': 'No speech detected. Please speak more clearly and try again',
      'Word not found in dictionary': 'This word is not supported yet. Please try another word',
      'Unable to connect to server': 'Unable to connect to server. Please check your connection and try again',
      'LLM API unavailable': 'Feedback generation is temporarily unavailable, but your score has been calculated',
    };

    // Check if message contains any of the error keys
    for (const [key, value] of Object.entries(errorMap)) {
      if (msg.includes(key)) {
        return value;
      }
    }

    return msg;
  };

  const friendlyMessage = getFriendlyMessage(message);

  return (
    <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 shadow-md">
      <div className="flex items-start gap-3">
        <span className="text-2xl">⚠️</span>
        <div className="flex-1">
          <h4 className="font-bold text-red-800 mb-1">Error</h4>
          <p className="text-red-700">{friendlyMessage}</p>
        </div>
        <div className="flex gap-2">
          {onRetry && (
            <button
              onClick={onRetry}
              className="text-red-600 hover:text-red-700 font-semibold text-sm"
            >
              Retry
            </button>
          )}
          {onDismiss && (
            <button
              onClick={onDismiss}
              className="text-red-600 hover:text-red-700 font-semibold text-sm"
            >
              Dismiss
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
