import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { pronunciationAPI } from '../services/api';
import ImageUploader from '../components/ImageUploader';
import ObjectDetectionDisplay from '../components/ObjectDetectionDisplay';
import AudioRecorder from '../components/AudioRecorder';
import ResultsDisplay from '../components/ResultsDisplay';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { DetectionResult, EvaluationResult } from '../types';

type ImageModeStep = 'upload' | 'detected' | 'recording' | 'results';

const ImageMode: React.FC = () => {
  const { userId } = useApp();
  const [step, setStep] = useState<ImageModeStep>('upload');
  const [detectionResult, setDetectionResult] = useState<DetectionResult | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = async (image: File) => {
    setError(null);
    setIsLoading(true);

    try {
      const result = await pronunciationAPI.detectObject(image, userId);
      setDetectionResult(result);
      setStep('detected');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to detect object in image');
    } finally {
      setIsLoading(false);
    }
  };

  const handleProceedToRecording = () => {
    setStep('recording');
  };

  const handleRecordingComplete = (blob: Blob) => {
    setAudioBlob(blob);
  };

  const handleEvaluate = async () => {
    if (!audioBlob || !detectionResult) {
      setError('Please record audio first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await pronunciationAPI.evaluatePronunciation(
        audioBlob,
        detectionResult.detected_object,
        userId,
        'image'
      );
      setEvaluationResult(result);
      setStep('results');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to evaluate pronunciation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setStep('upload');
    setDetectionResult(null);
    setAudioBlob(null);
    setEvaluationResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Image Mode</h2>
        <p className="text-gray-600 mb-8">
          Upload an image and practice pronouncing the detected object
        </p>

        {/* Step Indicator */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
              step === 'upload' ? 'bg-blue-600 text-white' : 'bg-green-500 text-white'
            }`}>
              1
            </div>
            <div className="w-16 h-1 bg-gray-300"></div>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
              step === 'upload' ? 'bg-gray-300 text-gray-600' :
              step === 'detected' || step === 'recording' ? 'bg-blue-600 text-white' :
              'bg-green-500 text-white'
            }`}>
              2
            </div>
            <div className="w-16 h-1 bg-gray-300"></div>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
              step === 'results' ? 'bg-green-500 text-white' : 'bg-gray-300 text-gray-600'
            }`}>
              3
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}

        {/* Step 1: Upload Image */}
        {step === 'upload' && (
          <div className="space-y-6">
            <ImageUploader onImageUpload={handleImageUpload} />
            {isLoading && <LoadingSpinner message="Detecting object in image..." />}
          </div>
        )}

        {/* Step 2: Object Detected - Record Pronunciation */}
        {(step === 'detected' || step === 'recording') && detectionResult && (
          <div className="space-y-6">
            <ObjectDetectionDisplay result={detectionResult} />

            {step === 'detected' && (
              <div className="flex justify-center">
                <button
                  onClick={handleProceedToRecording}
                  className="px-8 py-3 rounded-lg font-bold text-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                >
                  Start Recording
                </button>
              </div>
            )}

            {step === 'recording' && (
              <div className="bg-gray-50 rounded-lg p-6">
                <AudioRecorder onRecordingComplete={handleRecordingComplete} />
                
                {audioBlob && (
                  <div className="mt-6 flex justify-center">
                    <button
                      onClick={handleEvaluate}
                      disabled={isLoading}
                      className="px-8 py-3 rounded-lg font-bold text-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                    >
                      {isLoading ? 'Evaluating...' : 'Evaluate Pronunciation'}
                    </button>
                  </div>
                )}
              </div>
            )}

            {isLoading && <LoadingSpinner message="Analyzing your pronunciation..." />}
          </div>
        )}

        {/* Step 3: Results */}
        {step === 'results' && evaluationResult && (
          <div className="space-y-6">
            <ResultsDisplay result={evaluationResult} />

            <div className="flex justify-center gap-4">
              <button
                onClick={handleReset}
                className="px-8 py-3 rounded-lg font-bold text-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
              >
                Try Another Image
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageMode;
