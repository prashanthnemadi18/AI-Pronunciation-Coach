import React from 'react';
import { DetectionResult } from '../types';

interface ObjectDetectionDisplayProps {
  result: DetectionResult;
}

const ObjectDetectionDisplay: React.FC<ObjectDetectionDisplayProps> = ({ result }) => {
  const { detected_object, confidence, message } = result;

  const getConfidenceColor = (conf: number): string => {
    if (conf >= 0.8) return 'text-green-600';
    if (conf >= 0.6) return 'text-yellow-600';
    return 'text-orange-600';
  };

  const getConfidenceLabel = (conf: number): string => {
    if (conf >= 0.8) return 'High';
    if (conf >= 0.6) return 'Medium';
    return 'Low';
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-200">
      <div className="text-center space-y-4">
        <div className="text-5xl mb-2">🔍</div>
        
        <h3 className="text-2xl font-bold text-gray-800">
          Object Detected!
        </h3>
        
        <div className="bg-white rounded-lg p-4 shadow-md">
          <p className="text-sm text-gray-600 mb-2">Detected Object:</p>
          <p className="text-4xl font-bold text-blue-600 capitalize">
            {detected_object}
          </p>
        </div>

        <div className="flex items-center justify-center gap-2">
          <span className="text-sm text-gray-600">Confidence:</span>
          <span className={`text-lg font-bold ${getConfidenceColor(confidence)}`}>
            {(confidence * 100).toFixed(1)}%
          </span>
          <span className={`text-xs px-2 py-1 rounded-full ${
            confidence >= 0.8 ? 'bg-green-100 text-green-700' :
            confidence >= 0.6 ? 'bg-yellow-100 text-yellow-700' :
            'bg-orange-100 text-orange-700'
          }`}>
            {getConfidenceLabel(confidence)}
          </span>
        </div>

        <div className="bg-blue-100 border border-blue-300 rounded-lg p-4 mt-4">
          <p className="text-blue-800 font-semibold">
            {message}
          </p>
        </div>

        <div className="text-sm text-gray-500 mt-4">
          👇 Now record yourself pronouncing this word
        </div>
      </div>
    </div>
  );
};

export default ObjectDetectionDisplay;
