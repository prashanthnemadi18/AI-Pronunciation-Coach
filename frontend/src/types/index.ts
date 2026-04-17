// Type definitions for the AI Pronunciation Coach application

export type Mode = 'audio' | 'image' | 'game';

export interface PhonemeError {
  index: number;
  expected: string;
  actual: string;
  type: 'substitution' | 'missing' | 'extra';
}

export interface PhonemeComparison {
  matches: number[];
  errors: PhonemeError[];
}

export interface Feedback {
  correction_tips: string;
  encouragement: string;
}

export interface EvaluationResult {
  accuracy_score: number;
  transcribed_text: string;
  expected_phonemes: string[];
  actual_phonemes: string[];
  phoneme_comparison: PhonemeComparison;
  feedback: Feedback;
}

export interface DetectionResult {
  detected_object: string;
  confidence: number;
  message: string;
}

export interface PronunciationAttempt {
  id: number;
  target_word: string;
  accuracy_score: number;
  mode: Mode;
  created_at: string;
}

export interface HistoryResult {
  user_id: number;
  attempts: PronunciationAttempt[];
  total_attempts: number;
  average_score: number;
}

export interface LeaderboardEntry {
  user_id: number;
  username: string;
  total_score: number;
  words_attempted: number;
}

export interface LeaderboardResult {
  leaderboard: LeaderboardEntry[];
}

export interface AppState {
  currentMode: Mode;
  userId: number;
  isLoading: boolean;
  error: string | null;
}
