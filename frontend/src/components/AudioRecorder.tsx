import React, { useState, useRef, useEffect } from 'react';

interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void;
  maxDuration?: number;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onRecordingComplete,
  maxDuration = 5,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (audioURL) {
        URL.revokeObjectURL(audioURL);
      }
    };
  }, [audioURL]);

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);
        onRecordingComplete(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setDuration(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setDuration((prev) => {
          const newDuration = prev + 0.1;
          if (newDuration >= maxDuration) {
            stopRecording();
            return maxDuration;
          }
          return newDuration;
        });
      }, 100);
    } catch (err) {
      setError('Unable to access microphone. Please check permissions.');
      console.error('Error accessing microphone:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const resetRecording = () => {
    if (audioURL) {
      URL.revokeObjectURL(audioURL);
    }
    setAudioURL(null);
    setDuration(0);
    setError(null);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-center gap-4">
        {!isRecording && !audioURL && (
          <button
            onClick={startRecording}
            className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-200 flex items-center gap-2"
          >
            <span className="text-xl">🎤</span>
            <span>Start Recording</span>
          </button>
        )}

        {isRecording && (
          <button
            onClick={stopRecording}
            className="bg-gray-700 hover:bg-gray-800 text-white font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-200 flex items-center gap-2 animate-pulse"
          >
            <span className="text-xl">⏹️</span>
            <span>Stop Recording</span>
          </button>
        )}

        {audioURL && (
          <button
            onClick={resetRecording}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-full shadow-lg transition-all duration-200 flex items-center gap-2"
          >
            <span className="text-xl">🔄</span>
            <span>Record Again</span>
          </button>
        )}
      </div>

      {/* Duration Display */}
      {(isRecording || audioURL) && (
        <div className="text-center">
          <div className="inline-block bg-gray-100 px-6 py-2 rounded-full">
            <span className="text-2xl font-mono font-bold text-gray-700">
              {duration.toFixed(1)}s
            </span>
            <span className="text-gray-500 ml-2">/ {maxDuration}s</span>
          </div>
        </div>
      )}

      {/* Recording Indicator */}
      {isRecording && (
        <div className="flex items-center justify-center gap-2 text-red-600">
          <div className="w-3 h-3 bg-red-600 rounded-full animate-pulse"></div>
          <span className="font-semibold">Recording...</span>
        </div>
      )}

      {/* Audio Preview */}
      {audioURL && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600 mb-2">Preview:</p>
          <audio src={audioURL} controls className="w-full" />
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
