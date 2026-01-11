/**
 * Profile Store
 * State management for user profile using Zustand
 */

import { create } from 'zustand';
import { profileService, UserProfile, ProfileUpdateData } from '@/services/profile';

interface ProfileState {
  profile: UserProfile | null;
  loading: boolean;
  error: string | null;

  // Actions
  fetchProfile: () => Promise<void>;
  updateProfile: (data: ProfileUpdateData) => Promise<void>;
  clearProfile: () => void;
}

export const useProfileStore = create<ProfileState>((set) => ({
  profile: null,
  loading: false,
  error: null,

  fetchProfile: async () => {
    set({ loading: true, error: null });
    try {
      const profile = await profileService.getProfile();
      set({ profile, loading: false });
    } catch (error: any) {
      console.error('Failed to fetch profile:', error);
      set({ error: error.message || 'Failed to fetch profile', loading: false });
      throw error;
    }
  },

  updateProfile: async (data: ProfileUpdateData) => {
    set({ loading: true, error: null });
    try {
      const updatedProfile = await profileService.updateProfile(data);
      set({ profile: updatedProfile, loading: false });
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      set({ error: error.message || 'Failed to update profile', loading: false });
      throw error;
    }
  },

  clearProfile: () => {
    set({ profile: null, loading: false, error: null });
  },
}));
