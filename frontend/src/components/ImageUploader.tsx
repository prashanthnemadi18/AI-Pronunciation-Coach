import React, { useState, useRef } from 'react';

interface ImageUploaderProps {
  onImageUpload: (image: File) => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageUpload }) => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewURL, setPreviewURL] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const ALLOWED_FORMATS = ['image/jpeg', 'image/jpg', 'image/png'];
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

  const validateImageFile = (file: File): boolean => {
    // Check file type
    if (!ALLOWED_FORMATS.includes(file.type)) {
      setError('Please upload a valid image file (JPEG or PNG)');
      return false;
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      setError('Image file size must be less than 10MB');
      return false;
    }

    return true;
  };

  const handleFileSelect = (file: File) => {
    setError(null);
    
    const isValid = validateImageFile(file);
    if (isValid) {
      setSelectedImage(file);
      
      // Create preview URL
      const url = URL.createObjectURL(file);
      setPreviewURL(url);
      
      onImageUpload(file);
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
    if (previewURL) {
      URL.revokeObjectURL(previewURL);
    }
    setSelectedImage(null);
    setPreviewURL(null);
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
        accept="image/jpeg,image/jpg,image/png"
        onChange={handleFileInputChange}
        className="hidden"
      />

      {!selectedImage ? (
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
            <div className="text-5xl">🖼️</div>
            <p className="text-lg font-semibold text-gray-700">
              Drop image here or click to browse
            </p>
            <p className="text-sm text-gray-500">
              Supported formats: JPEG, PNG (max 10MB)
            </p>
          </div>
        </div>
      ) : (
        <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
          <div className="space-y-4">
            {/* Image Preview */}
            {previewURL && (
              <div className="relative">
                <img
                  src={previewURL}
                  alt="Preview"
                  className="w-full h-64 object-contain rounded-lg bg-gray-50"
                />
              </div>
            )}
            
            {/* File Info */}
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-gray-800">{selectedImage.name}</p>
                <p className="text-sm text-gray-600">
                  {(selectedImage.size / 1024).toFixed(1)} KB
                </p>
              </div>
              <button
                onClick={handleReset}
                className="text-red-600 hover:text-red-700 font-semibold"
              >
                Remove
              </button>
            </div>
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

export default ImageUploader;
