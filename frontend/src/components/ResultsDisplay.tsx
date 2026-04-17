import React from 'react';
import { EvaluationResult } from '../types';

interface ResultsDisplayProps {
  result: EvaluationResult;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result }) => {
  const {
    accuracy_score,
    transcribed_text,
    expected_phonemes,
    actual_phonemes,
    phoneme_comparison,
    feedback,
  } = result;

  const getScoreColor = (score: number): string => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreGradient = (score: number): string => {
    if (score >= 90) return 'from-green-500 to-green-600';
    if (score >= 70) return 'from-yellow-500 to-yellow-600';
    return 'from-red-500 to-red-600';
  };

  const isPhonemeCorrect = (index: number): boolean => {
    return phoneme_comparison.matches.includes(index);
  };

  const getPhonemeError = (index: number) => {
    return phoneme_comparison.errors.find(error => error.index === index);
  };

  return (
    <div className="space-y-6">
      {/* Score Display */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
          Pronunciation Score
        </h3>
        <div className="flex flex-col items-center">
          <div className={`text-6xl font-bold ${getScoreColor(accuracy_score)} mb-2`}>
            {accuracy_score.toFixed(1)}%
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
            <div
              className={`h-4 rounded-full bg-gradient-to-r ${getScoreGradient(accuracy_score)} transition-all duration-500`}
              style={{ width: `${accuracy_score}%` }}
            ></div>
          </div>
          <p className="text-gray-600">
            You said: <span className="font-semibold">{transcribed_text}</span>
          </p>
        </div>
      </div>

      {/* Phoneme Comparison */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          Phoneme Analysis
        </h3>
        
        <div className="space-y-4">
          {/* Expected Phonemes */}
          <div>
            <p className="text-sm font-semibold text-gray-600 mb-2">Expected:</p>
            <div className="flex flex-wrap gap-2">
              {expected_phonemes.map((phoneme, index) => {
                const isCorrect = isPhonemeCorrect(index);
                const error = getPhonemeError(index);
                
                return (
                  <div
                    key={`expected-${index}`}
                    className={`
                      px-3 py-2 rounded-lg font-mono font-bold text-sm
                      ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                    `}
                    title={error ? `Error: ${error.type}` : 'Correct'}
                  >
                    {phoneme}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Actual Phonemes */}
          <div>
            <p className="text-sm font-semibold text-gray-600 mb-2">Your pronunciation:</p>
            <div className="flex flex-wrap gap-2">
              {actual_phonemes.map((phoneme, index) => {
                const isCorrect = isPhonemeCorrect(index);
                const error = getPhonemeError(index);
                
                return (
                  <div
                    key={`actual-${index}`}
                    className={`
                      px-3 py-2 rounded-lg font-mono font-bold text-sm
                      ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                    `}
                    title={error ? `Expected: ${error.expected}` : 'Correct'}
                  >
                    {phoneme}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Error Details */}
          {phoneme_comparison.errors.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm font-semibold text-yellow-800 mb-2">
                Errors detected:
              </p>
              <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700">
                {phoneme_comparison.errors.map((error, index) => (
                  <li key={index}>
                    Position {error.index + 1}: Expected "{error.expected}", got "{error.actual}"
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Feedback */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          Feedback & Tips
        </h3>
        
        <div className="space-y-4">
          {/* Correction Tips */}
          {feedback.correction_tips && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm font-semibold text-blue-800 mb-2">
                💡 How to improve:
              </p>
              <p className="text-blue-700">{feedback.correction_tips}</p>
            </div>
          )}

          {/* Encouragement */}
          {feedback.encouragement && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-sm font-semibold text-green-800 mb-2">
                ✨ Keep it up!
              </p>
              <p className="text-green-700">{feedback.encouragement}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
