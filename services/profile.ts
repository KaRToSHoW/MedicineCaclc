/**
 * Profile API Service
 * Handles profile-related API calls
 */

import { api } from './api';
import { API_BASE_URL } from '../config/api';

export interface ProfileUpdateData {
  name?: string;
  email?: string;
}

export interface UserProfile {
  id: string;
  email: string;
  name?: string;
  firebaseUid: string;
  createdAt?: string;
}

class ProfileService {
  /**
   * Get current user profile
   */
  async getProfile(): Promise<UserProfile> {
    return api.get<UserProfile>(`${API_BASE_URL}/api/v1/profiles/me`);
  }

  /**
   * Update current user profile
   */
  async updateProfile(data: ProfileUpdateData): Promise<UserProfile> {
    return api.patch<UserProfile>(`${API_BASE_URL}/api/v1/profiles/me`, data);
  }
}

export const profileService = new ProfileService();
