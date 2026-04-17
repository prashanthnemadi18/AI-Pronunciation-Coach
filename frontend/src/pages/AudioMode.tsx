import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { pronunciationAPI } from '../services/api';
import AudioRecorder from '../components/AudioRecorder';
import AudioUploader from '../components/AudioUploader';
import TargetWordInput from '../components/TargetWordInput';
import ResultsDisplay from '../components/ResultsDisplay';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { EvaluationResult } from '../types';

const AudioMode: React.FC = () => {
  const { userId } = useApp();
  const [targetWord, setTargetWord] = useState('');
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [inputMethod, setInputMethod] = useState<'record' | 'upload'>('record');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EvaluationResult | null>(null);

  const handleRecordingComplete = (blob: Blob) => {
    setAudioBlob(blob);
    setError(null);
  };

  const handleAudioUpload = (blob: Blob) => {
    setAudioBlob(blob);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!audioBlob) {
      setError('Please record or upload audio first');
      return;
    }

    if (!targetWord.trim()) {
      setError('Please enter a target word');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const evaluationResult = await pronunciationAPI.evaluatePronunciation(
        audioBlob,
        targetWord.trim(),
        userId,
        'audio'
      );
      setResult(evaluationResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate pronunciation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAudioBlob(null);
    setResult(null);
    setError(null);
    setTargetWord('');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-3xl shadow-sm p-10 border border-gray-100">
        {!result ? (
          <div className="space-y-8">
            {/* Target Word Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Target Word
              </label>
              <TargetWordInput
                value={targetWord}
                onChange={setTargetWord}
                disabled={isLoading}
              />
            </div>

            {/* Input Method Selector */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Choose Input Method
              </label>
              <div className="flex gap-4">
                <button
                  onClick={() => setInputMethod('record')}
                  className={`
                    flex-1 px-6 py-4 rounded-2xl font-semibold transition-all duration-200 flex items-center justify-center gap-3
                    ${
                      inputMethod === 'record'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-md'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                    }
                  `}
                >
                  <span className="text-2xl">🎤</span>
                  <span>Record Audio</span>
                </button>
                <button
                  onClick={() => setInputMethod('upload')}
                  className={`
                    flex-1 px-6 py-4 rounded-2xl font-semibold transition-all duration-200 flex items-center justify-center gap-3
                    ${
                      inputMethod === 'upload'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-md'
                        : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                    }
                  `}
                >
                  <span className="text-2xl">📁</span>
                  <span>Upload Audio</span>
                </button>
              </div>
            </div>

            {/* Audio Input Component */}
            <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-8 border border-gray-100">
              {inputMethod === 'record' ? (
                <AudioRecorder onRecordingComplete={handleRecordingComplete} />
              ) : (
                <AudioUploader onAudioUpload={handleAudioUpload} />
              )}
            </div>

            {/* Error Display */}
            {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

            {/* Submit Button */}
            <div className="flex justify-center pt-4">
              <button
                onClick={handleSubmit}
                disabled={!audioBlob || !targetWord.trim() || isLoading}
                className={`
                  px-10 py-4 rounded-2xl font-bold text-lg transition-all duration-200 shadow-md
                  ${
                    audioBlob && targetWord.trim() && !isLoading
                      ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:shadow-xl transform hover:scale-105'
                      : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  }
                `}
              >
                {isLoading ? 'Evaluating...' : 'Evaluate Pronunciation'}
              </button>
            </div>

            {/* Loading Spinner */}
            {isLoading && <LoadingSpinner message="Analyzing your pronunciation..." />}
          </div>
        ) : (
          <div className="space-y-8">
            {/* Results Display */}
            <ResultsDisplay result={result} />

            {/* Action Buttons */}
            <div className="flex justify-center gap-4 pt-4">
              <button
                onClick={handleReset}
                className="px-10 py-4 rounded-2xl font-bold text-lg bg-gradient-to-r from-blue-500 to-indigo-600 text-white hover:shadow-xl transform hover:scale-105 transition-all duration-200 shadow-md"
              >
                Try Another Word
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AudioMode;
