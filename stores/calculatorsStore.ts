/**
 * Calculators Store
 * Zustand store for managing calculators state
 * Updated to use static data from JSON file
 */

import { create } from 'zustand';
import type { Calculator } from '@/types/calculators';
import calculatorsData from '@/data/calculators-static.json';

interface CalculatorsStore {
  // State
  items: Calculator[];
  loading: boolean;
  error: string | null;

  // Actions
  fetchAll: () => Promise<void>;
  reset: () => void;
}

export const useCalculatorsStore = create<CalculatorsStore>((set) => ({
  items: [],
  loading: false,
  error: null,

  fetchAll: async () => {
    set({ loading: true, error: null });
    try {
      // Load static data from JSON file
      const items = calculatorsData.map((calc: any) => ({
        ...calc,
        id: String(calc.id),
        category: calc.category || '',
        categoryId: String(calc.category || '').toLowerCase(),
      }));
      
      set({ items: items as Calculator[], loading: false });
    } catch (error: any) {
      console.error('Failed to load calculators:', error);
      set({ error: error.message || 'Failed to load calculators', loading: false });
    }
  },

  reset: () => set({ items: [], loading: false, error: null }),
}));
