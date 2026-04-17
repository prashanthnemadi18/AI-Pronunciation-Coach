import React, { useState } from 'react';

interface TargetWordInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const TargetWordInput: React.FC<TargetWordInputProps> = ({
  value,
  onChange,
  disabled = false,
}) => {
  const [error, setError] = useState<string | null>(null);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    onChange(newValue);
    
    // Validate input
    if (newValue.trim() === '') {
      setError('Please enter a word to practice');
    } else if (!/^[a-zA-Z\s-]+$/.test(newValue)) {
      setError('Please use only letters, spaces, and hyphens');
    } else {
      setError(null);
    }
  };

  return (
    <div className="space-y-2">
      <label htmlFor="target-word" className="block text-sm font-semibold text-gray-700">
        Target Word
      </label>
      <input
        id="target-word"
        type="text"
        value={value}
        onChange={handleChange}
        disabled={disabled}
        placeholder="Enter a word to practice (e.g., hello)"
        className={`
          w-full px-4 py-3 rounded-lg border-2 text-lg
          focus:outline-none focus:ring-2 focus:ring-blue-500
          transition-all duration-200
          ${error ? 'border-red-300' : 'border-gray-300'}
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
      />
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      <p className="text-xs text-gray-500">
        Enter the word you want to practice pronouncing
      </p>
    </div>
  );
};

export default TargetWordInput;
