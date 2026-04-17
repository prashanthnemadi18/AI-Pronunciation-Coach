import React, { useState, useRef } from 'react';

interface AudioUploaderProps {
  onAudioUpload: (audioBlob: Blob) => void;
  maxDuration?: number;
}

const AudioUploader: React.FC<AudioUploaderProps> = ({
  onAudioUpload,
  maxDuration = 5,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const ALLOWED_FORMATS = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/x-m4a', 'audio/m4a'];
  const ALLOWED_EXTENSIONS = ['.wav', '.mp3', '.m4a'];

  const validateAudioFile = async (file: File): Promise<boolean> => {
    // Check file type
    const isValidType = ALLOWED_FORMATS.includes(file.type) || 
                       ALLOWED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!isValidType) {
      setError('Please upload a valid audio file (WAV, MP3, or M4A)');
      return false;
    }

    // Check duration
    try {
      const duration = await getAudioDuration(file);
      if (duration > maxDuration) {
        setError(`Audio must be ${maxDuration} seconds or less (current: ${duration.toFixed(1)}s)`);
        return false;
      }
    } catch (err) {
      console.error('Error checking audio duration:', err);
      // Continue anyway if we can't check duration
    }

    return true;
  };

  const getAudioDuration = (file: File): Promise<number> => {
    return new Promise((resolve, reject) => {
      const audio = new Audio();
      audio.preload = 'metadata';
      
      audio.onloadedmetadata = () => {
        URL.revokeObjectURL(audio.src);
        resolve(audio.duration);
      };
      
      audio.onerror = () => {
        URL.revokeObjectURL(audio.src);
        reject(new Error('Failed to load audio metadata'));
      };
      
      audio.src = URL.createObjectURL(file);
    });
  };

  const handleFileSelect = async (file: File) => {
    setError(null);
    
    const isValid = await validateAudioFile(file);
    if (isValid) {
      setSelectedFile(file);
      onAudioUpload(file);
    }
  };

  const handleFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    
    const file = event.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setSelectedFile(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-4">
      <input
        ref={fileInputRef}
        type="file"
        accept=".wav,.mp3,.m4a,audio/wav,audio/mpeg,audio/mp3,audio/x-m4a,audio/m4a"
        onChange={handleFileInputChange}
        className="hidden"
      />

      {!selectedFile ? (
        <div
          onClick={handleClick}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            transition-all duration-200
            ${
              isDragging
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            }
          `}
        >
          <div className="space-y-2">
            <div className="text-5xl">📁</div>
            <p className="text-lg font-semibold text-gray-700">
              Drop audio file here or click to browse
            </p>
            <p className="text-sm text-gray-500">
              Supported formats: WAV, MP3, M4A (max {maxDuration}s)
            </p>
          </div>
        </div>
      ) : (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-3xl">🎵</span>
              <div>
                <p className="font-semibold text-gray-800">{selectedFile.name}</p>
                <p className="text-sm text-gray-600">
                  {(selectedFile.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <button
              onClick={handleReset}
              className="text-red-600 hover:text-red-700 font-semibold"
            >
              Remove
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
};

export default AudioUploader;
