import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  EvaluationResult,
  DetectionResult,
  HistoryResult,
  LeaderboardResult,
  Mode,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class PronunciationAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 seconds
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: AxiosError): Error {
    if (error.response) {
      // Server responded with error status
      const detail = (error.response.data as any)?.detail || 'An error occurred';
      return new Error(detail);
    } else if (error.request) {
      // Request made but no response
      return new Error('Unable to connect to server. Please check your connection.');
    } else {
      // Something else happened
      return new Error(error.message || 'An unexpected error occurred');
    }
  }

  async evaluatePronunciation(
    audio: Blob,
    targetWord: string,
    userId: number,
    mode: Mode = 'audio'
  ): Promise<EvaluationResult> {
    // Convert audio blob to base64
    const base64Audio = await this.blobToBase64(audio);
    
    const response = await this.client.post<EvaluationResult>(
      '/api/pronunciation/evaluate',
      {
        audio: base64Audio,
        target_word: targetWord,
        user_id: userId,
        mode: mode,
        audio_format: 'wav',
      }
    );

    return response.data;
  }

  async detectObject(image: File, userId?: number): Promise<DetectionResult> {
    const formData = new FormData();
    formData.append('image', image);
    if (userId) {
      formData.append('user_id', userId.toString());
    }

    const response = await this.client.post<DetectionResult>(
      '/api/pronunciation/image',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  }

  async getUserHistory(userId: number, limit: number = 50): Promise<HistoryResult> {
    const response = await this.client.get<HistoryResult>(
      `/api/user/${userId}/history`,
      {
        params: { limit },
      }
    );

    return response.data;
  }

  async getLeaderboard(limit: number = 10): Promise<LeaderboardResult> {
    const response = await this.client.get<LeaderboardResult>(
      '/api/leaderboard',
      {
        params: { limit },
      }
    );

    return response.data;
  }

  async healthCheck(): Promise<any> {
    const response = await this.client.get('/api/health');
    return response.data;
  }

  private blobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        // Remove the data URL prefix (e.g., "data:audio/wav;base64,")
        const base64Data = base64String.split(',')[1];
        resolve(base64Data);
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
}

// Export singleton instance
export const pronunciationAPI = new PronunciationAPI();
