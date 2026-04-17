import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Mode, AppState } from '../types';

interface AppContextType extends AppState {
  setMode: (mode: Mode) => void;
  setUserId: (userId: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentMode, setCurrentMode] = useState<Mode>('audio');
  const [userId, setUserId] = useState<number>(1); // Default user ID
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const value: AppContextType = {
    currentMode,
    userId,
    isLoading,
    error,
    setMode: setCurrentMode,
    setUserId,
    setLoading: setIsLoading,
    setError,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
