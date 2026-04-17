import React from 'react';
import { useNavigate } from 'react-router-dom';

const ModeSelector: React.FC = () => {
  const navigate = useNavigate();

  const modes = [
    {
      id: 'audio',
      title: 'Audio Mode',
      description: 'Record or upload audio to practice pronunciation',
      icon: '🎤',
      path: '/audio',
      gradient: 'from-blue-500 to-indigo-600',
    },
    {
      id: 'image',
      title: 'Image Mode',
      description: 'Identify objects and practice their pronunciation',
      icon: '📸',
      path: '/image',
      gradient: 'from-emerald-500 to-teal-600',
    },
    {
      id: 'game',
      title: 'Game Mode',
      description: 'Challenge yourself with timed pronunciation games',
      icon: '🎮',
      path: '/game',
      gradient: 'from-purple-500 to-pink-600',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {modes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => navigate(mode.path)}
            className="group relative bg-white rounded-3xl shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:scale-105 p-8 text-left border border-gray-100 overflow-hidden"
          >
            {/* Gradient background on hover */}
            <div className={`absolute inset-0 bg-gradient-to-br ${mode.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
            
            {/* Icon */}
            <div className={`relative inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${mode.gradient} rounded-2xl mb-6 shadow-md group-hover:shadow-lg transition-all`}>
              <span className="text-3xl">{mode.icon}</span>
            </div>
            
            {/* Content */}
            <div className="relative">
              <h3 className="text-2xl font-bold text-gray-900 mb-3">
                {mode.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed mb-6">
                {mode.description}
              </p>
              
              {/* Arrow */}
              <div className="flex items-center text-gray-400 group-hover:text-gray-900 transition-colors">
                <span className="text-sm font-semibold">Get Started</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModeSelector;
